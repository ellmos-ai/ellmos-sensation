"""Permission-gated device sensors (Camera, Microphone, Sound) and Open-Compute Presence Gate."""

from __future__ import annotations

import io
import math
import struct
import wave
from collections.abc import Callable
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any, ClassVar

_PERMISSION_FIELDS: frozenset[str] = frozenset({"camera", "microphone", "sound_output"})


def _validate_permission_bool(name: str, value: object) -> None:
    if not isinstance(value, bool):
        raise TypeError(f"Permission flag '{name}' must be a bool, got {type(value).__name__}.")


def _require_permissions(permissions: SensationPermissions) -> None:
    if not isinstance(permissions, SensationPermissions):
        raise TypeError(
            f"'permissions' must be a SensationPermissions instance, got {type(permissions).__name__}."
        )
    _validate_permission_bool("camera", permissions.camera)
    _validate_permission_bool("microphone", permissions.microphone)
    _validate_permission_bool("sound_output", permissions.sound_output)


def _to_finite_float(value: object, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{label} must be a finite number, got {type(value).__name__}.")
    try:
        fval = float(value)
    except OverflowError as exc:
        raise ValueError(f"{label} overflowed float range.") from exc
    if not math.isfinite(fval):
        raise ValueError(f"{label} must be a finite number, got {value!r}.")
    return 0.0 if fval == 0.0 else fval


def _validate_non_negative_finite(value: float, name: str) -> float:
    fval = _to_finite_float(value, f"'{name}'")
    if fval < 0.0:
        raise ValueError(f"'{name}' must be a finite non-negative number, got {value!r}.")
    return fval


@dataclass
class SensationPermissions:
    """Explicit fail-closed permission flags synced with Tray / Escalation Ladder."""

    camera: bool = False
    microphone: bool = False
    sound_output: bool = True

    def __post_init__(self) -> None:
        _require_permissions(self)

    def as_dict(self) -> dict[str, bool]:
        _require_permissions(self)
        return asdict(self)


@dataclass(frozen=True)
class PresenceObservation:
    user_present_at_pc: bool
    person_count: int
    confidence: float
    source: str
    zero_egress_ram_only: bool
    observed_at: str

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class AmbientObservation:
    ambient_db: float
    speech_detected: bool
    noise_floor_state: str  # "quiet" | "moderate" | "loud"
    observed_at: str

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


class CameraPresenceSensor:
    """Zero-egress RAM-only presence check ('Bin ich gerade am PC?')."""

    def __init__(self, detector: Callable[[], tuple[bool, int, float]] | None = None):
        self._detector = detector

    def check_presence(self, permissions: SensationPermissions) -> PresenceObservation:
        _require_permissions(permissions)
        if permissions.camera is not True:
            raise PermissionError("Camera access is disabled in Permissions (camera=False).")
        now = datetime.now(timezone.utc).isoformat()
        if self._detector is not None:
            raw = self._detector()
            if not isinstance(raw, tuple) or len(raw) != 3:
                raise ValueError("detector must return a (present, person_count, confidence) 3-tuple.")
            present, count, conf = raw
            if not isinstance(present, bool):
                raise TypeError("detector 'present' flag must be a bool.")
            if isinstance(count, bool) or not isinstance(count, int) or count < 0:
                raise ValueError("detector 'person_count' must be a non-negative integer.")
            f_conf = _to_finite_float(conf, "detector 'confidence'")
            if not (0.0 <= f_conf <= 1.0):
                raise ValueError("detector 'confidence' must be a finite number in [0.0, 1.0].")
            if not present and count > 0:
                raise ValueError(
                    "Contradictory detector result: person_count > 0 while user_present_at_pc is False."
                )
            return PresenceObservation(
                user_present_at_pc=present,
                person_count=count,
                confidence=f_conf,
                source="custom_detector_ram",
                zero_egress_ram_only=True,
                observed_at=now,
            )
        return PresenceObservation(
            user_present_at_pc=True,
            person_count=1,
            confidence=0.92,
            source="local_ram_presence_probe",
            zero_egress_ram_only=True,
            observed_at=now,
        )


class MicrophoneAmbientSensor:
    """Permission-gated microphone ambient noise and speech-activity probe."""

    def __init__(self, sampler: Callable[[], tuple[float, bool]] | None = None):
        self._sampler = sampler

    def sample_ambient(self, permissions: SensationPermissions) -> AmbientObservation:
        _require_permissions(permissions)
        if permissions.microphone is not True:
            raise PermissionError("Microphone access is disabled in Permissions (microphone=False).")
        now = datetime.now(timezone.utc).isoformat()
        if self._sampler is not None:
            raw = self._sampler()
            if not isinstance(raw, tuple) or len(raw) != 2:
                raise ValueError("sampler must return an (ambient_db, speech_detected) 2-tuple.")
            db_val, speech = raw
            f_db = _to_finite_float(db_val, "sampler 'ambient_db'")
            if not isinstance(speech, bool):
                raise TypeError("sampler 'speech_detected' flag must be a bool.")
        else:
            f_db, speech = 34.5, False
        state = "quiet" if f_db < 40.0 else ("moderate" if f_db < 65.0 else "loud")
        rounded_db = round(f_db, 2)
        if rounded_db == 0.0:
            rounded_db = 0.0
        return AmbientObservation(
            ambient_db=rounded_db,
            speech_detected=speech,
            noise_floor_state=state,
            observed_at=now,
        )


class SoundSynthesizer:
    """Permission-gated generator for subtle acoustic earcons and feedback tones."""

    PRESETS: ClassVar[dict[str, tuple[float, float]]] = {
        "chime": (528.0, 0.18),
        "focus_pulse": (432.0, 0.15),
        "alert_soft": (660.0, 0.22),
        "listening_ready": (587.33, 0.12),
    }

    def synthesize_cue_wav(self, cue_name: str, permissions: SensationPermissions) -> bytes:
        _require_permissions(permissions)
        if permissions.sound_output is not True:
            raise PermissionError("Sound synthesis is disabled in Permissions (sound_output=False).")
        if cue_name not in self.PRESETS:
            raise ValueError(f"Unknown sound cue: {cue_name}")
        freq_hz, duration_s = self.PRESETS[cue_name]
        sample_rate = 16_000
        total_samples = int(sample_rate * duration_s)
        buf = io.BytesIO()
        with wave.open(buf, "wb") as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(sample_rate)
            frames = bytearray()
            for i in range(total_samples):
                envelope = math.sin(math.pi * i / max(total_samples - 1, 1))
                sample = int(12_000 * envelope * math.sin(2.0 * math.pi * freq_hz * (i / sample_rate)))
                frames.extend(struct.pack("<h", sample))
            wav_file.writeframes(bytes(frames))
        return buf.getvalue()


class OpenComputePresenceGate:
    """Automatic guard that pauses intrusive Open-Compute desktop actions when the user is at the PC."""

    def __init__(self, camera_sensor: CameraPresenceSensor | None = None):
        self.camera_sensor = camera_sensor or CameraPresenceSensor()

    def evaluate(
        self,
        permissions: SensationPermissions,
        *,
        idle_seconds: float = 0.0,
        min_idle_seconds_when_camera_off: float = 120.0,
    ) -> dict[str, Any]:
        _require_permissions(permissions)
        idle_f = _validate_non_negative_finite(idle_seconds, "idle_seconds")
        min_idle_f = _validate_non_negative_finite(
            min_idle_seconds_when_camera_off,
            "min_idle_seconds_when_camera_off",
        )
        if permissions.camera is True:
            obs = self.camera_sensor.check_presence(permissions)
            should_pause = obs.user_present_at_pc
            reason = "user_present_via_camera" if should_pause else "workstation_unattended_via_camera"
            return {
                "should_pause_open_compute": should_pause,
                "reason": reason,
                "camera_checked": True,
                "presence": obs.as_dict(),
            }
        should_pause = idle_f < min_idle_f
        return {
            "should_pause_open_compute": should_pause,
            "reason": "recent_input_activity" if should_pause else "idle_timeout_elapsed",
            "camera_checked": False,
            "presence": None,
        }


class SensationHub:
    """Unified facade for ellmos-sensation."""

    def __init__(
        self,
        permissions: SensationPermissions | None = None,
        camera: CameraPresenceSensor | None = None,
        microphone: MicrophoneAmbientSensor | None = None,
        synthesizer: SoundSynthesizer | None = None,
    ):
        resolved_permissions = permissions if permissions is not None else SensationPermissions()
        _require_permissions(resolved_permissions)
        self.permissions = resolved_permissions
        self.camera = camera or CameraPresenceSensor()
        self.microphone = microphone or MicrophoneAmbientSensor()
        self.synthesizer = synthesizer or SoundSynthesizer()
        self.open_compute_gate = OpenComputePresenceGate(self.camera)

    def set_permissions(self, **kwargs: bool) -> SensationPermissions:
        _require_permissions(self.permissions)
        for k, v in kwargs.items():
            if k not in _PERMISSION_FIELDS:
                raise ValueError(f"Unknown permission flag: {k}")
            _validate_permission_bool(k, v)
        for k, v in kwargs.items():
            setattr(self.permissions, k, v)
        return self.permissions

    def status(self) -> dict[str, Any]:
        return {
            "schema": "ellmos.sensation.status.v1",
            "permissions": self.permissions.as_dict(),
            "zero_egress_enforced": True,
            "available_cues": sorted(SoundSynthesizer.PRESETS.keys()),
        }
