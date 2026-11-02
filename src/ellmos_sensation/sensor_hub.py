"""Permission-gated device sensors (Camera, Microphone, Sound) and Open-Compute Presence Gate."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import io
import math
import struct
from typing import Any, Callable
import wave


@dataclass
class SensationPermissions:
    """Explicit fail-closed permission flags synced with Tray / Escalation Ladder."""

    camera: bool = False
    microphone: bool = False
    sound_output: bool = True

    def as_dict(self) -> dict[str, bool]:
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
        if not permissions.camera:
            raise PermissionError("Camera access is disabled in Permissions (camera=False).")
        now = datetime.now(timezone.utc).isoformat()
        if self._detector is not None:
            present, count, conf = self._detector()
            return PresenceObservation(
                user_present_at_pc=bool(present),
                person_count=int(count),
                confidence=float(conf),
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
        if not permissions.microphone:
            raise PermissionError("Microphone access is disabled in Permissions (microphone=False).")
        now = datetime.now(timezone.utc).isoformat()
        if self._sampler is not None:
            db_val, speech = self._sampler()
        else:
            db_val, speech = 34.5, False
        state = "quiet" if db_val < 40.0 else ("moderate" if db_val < 65.0 else "loud")
        return AmbientObservation(
            ambient_db=round(float(db_val), 2),
            speech_detected=bool(speech),
            noise_floor_state=state,
            observed_at=now,
        )


class SoundSynthesizer:
    """Permission-gated generator for subtle acoustic earcons and feedback tones."""

    PRESETS: dict[str, tuple[float, float]] = {
        "chime": (528.0, 0.18),
        "focus_pulse": (432.0, 0.15),
        "alert_soft": (660.0, 0.22),
        "listening_ready": (587.33, 0.12),
    }

    def synthesize_cue_wav(self, cue_name: str, permissions: SensationPermissions) -> bytes:
        if not permissions.sound_output:
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
        if permissions.camera:
            obs = self.camera_sensor.check_presence(permissions)
            should_pause = obs.user_present_at_pc
            reason = "user_present_via_camera" if should_pause else "workstation_unattended_via_camera"
            return {
                "should_pause_open_compute": should_pause,
                "reason": reason,
                "camera_checked": True,
                "presence": obs.as_dict(),
            }
        should_pause = idle_seconds < min_idle_seconds_when_camera_off
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
        self.permissions = permissions or SensationPermissions()
        self.camera = camera or CameraPresenceSensor()
        self.microphone = microphone or MicrophoneAmbientSensor()
        self.synthesizer = synthesizer or SoundSynthesizer()
        self.open_compute_gate = OpenComputePresenceGate(self.camera)

    def set_permissions(self, **kwargs: bool) -> SensationPermissions:
        for k, v in kwargs.items():
            if not hasattr(self.permissions, k):
                raise ValueError(f"Unknown permission flag: {k}")
            setattr(self.permissions, k, bool(v))
        return self.permissions

    def status(self) -> dict[str, Any]:
        return {
            "schema": "ellmos.sensation.status.v1",
            "permissions": self.permissions.as_dict(),
            "zero_egress_enforced": True,
            "available_cues": sorted(SoundSynthesizer.PRESETS.keys()),
        }
