"""Tests for ellmos-sensation permission gates, sensors, and Open-Compute presence gate."""

from __future__ import annotations

import json
import math

import pytest

from ellmos_sensation import (
    CameraPresenceSensor,
    MicrophoneAmbientSensor,
    OpenComputePresenceGate,
    SensationHub,
    SensationPermissions,
)
from ellmos_sensation.cli import main


def test_camera_and_microphone_fail_closed_by_default():
    hub = SensationHub()
    assert hub.permissions.camera is False
    assert hub.permissions.microphone is False
    with pytest.raises(PermissionError, match="camera=False"):
        hub.camera.check_presence(hub.permissions)
    with pytest.raises(PermissionError, match="microphone=False"):
        hub.microphone.sample_ambient(hub.permissions)


def test_camera_presence_and_open_compute_gate():
    sensor = CameraPresenceSensor(detector=lambda: (True, 1, 0.98))
    hub = SensationHub(permissions=SensationPermissions(camera=True), camera=sensor)
    gate = hub.open_compute_gate.evaluate(hub.permissions)
    assert gate["should_pause_open_compute"] is True
    assert gate["reason"] == "user_present_via_camera"
    assert gate["presence"]["zero_egress_ram_only"] is True


def test_open_compute_gate_unattended_allows_execution():
    sensor = CameraPresenceSensor(detector=lambda: (False, 0, 0.99))
    hub = SensationHub(permissions=SensationPermissions(camera=True), camera=sensor)
    gate = hub.open_compute_gate.evaluate(hub.permissions)
    assert gate["should_pause_open_compute"] is False
    assert gate["reason"] == "workstation_unattended_via_camera"


def test_sound_synthesizer_generates_valid_wav():
    hub = SensationHub(permissions=SensationPermissions(sound_output=True))
    wav_bytes = hub.synthesizer.synthesize_cue_wav("chime", hub.permissions)
    assert wav_bytes[:4] == b"RIFF"
    assert len(wav_bytes) > 100
    hub.set_permissions(sound_output=False)
    with pytest.raises(PermissionError, match="sound_output=False"):
        hub.synthesizer.synthesize_cue_wav("chime", hub.permissions)


def test_cli_status_and_gate(capsys):
    assert main(["status"]) == 0
    out = json.loads(capsys.readouterr().out)
    assert out["schema"] == "ellmos.sensation.status.v1"

    assert main(["open-compute-gate", "--allow-camera"]) == 0
    gate_out = json.loads(capsys.readouterr().out)
    assert gate_out["camera_checked"] is True


def test_permissions_reject_non_bool_and_method_overwrite():
    for bad_val in ("false", "true", "0", 0, 1, None):
        with pytest.raises(TypeError):
            SensationPermissions(camera=bad_val)  # type: ignore[arg-type]
        with pytest.raises(TypeError):
            SensationPermissions(microphone=bad_val)  # type: ignore[arg-type]
        with pytest.raises(TypeError):
            SensationPermissions(sound_output=bad_val)  # type: ignore[arg-type]

    hub = SensationHub()
    with pytest.raises(TypeError):
        hub.set_permissions(camera="false")  # type: ignore[arg-type]
    assert hub.permissions.camera is False

    # Atomic fail-closed update: valid flag must not stay mutated when another arg is invalid
    with pytest.raises(TypeError):
        hub.set_permissions(camera=True, microphone="false")  # type: ignore[arg-type]
    assert hub.permissions.camera is False

    # Method attributes like as_dict must not be writable via set_permissions
    with pytest.raises(ValueError, match="Unknown permission flag"):
        hub.set_permissions(as_dict=False)
    assert callable(hub.permissions.as_dict)
    assert hub.status()["permissions"]["camera"] is False

    # Direct post-init attribute tampering must also fail closed across all entrypoints
    tampered = SensationPermissions()
    tampered.camera = "false"  # type: ignore[assignment]
    with pytest.raises(TypeError):
        hub.camera.check_presence(tampered)
    tampered_sound = SensationPermissions()
    tampered_sound.sound_output = "false"  # type: ignore[assignment]
    with pytest.raises(TypeError):
        hub.synthesizer.synthesize_cue_wav("chime", tampered_sound)


def test_open_compute_gate_rejects_nan_inf_negative_overflow_and_bool_inputs(capsys):
    gate = OpenComputePresenceGate()
    perms_off = SensationPermissions(camera=False)
    perms_on = SensationPermissions(camera=True)

    for bad_num in (float("nan"), float("inf"), float("-inf"), -0.001, -120.0, 10**400):
        with pytest.raises(ValueError):
            gate.evaluate(perms_off, idle_seconds=bad_num)
        with pytest.raises(ValueError):
            gate.evaluate(perms_off, min_idle_seconds_when_camera_off=bad_num)
        with pytest.raises(ValueError):
            gate.evaluate(perms_on, idle_seconds=bad_num)

    for bad_type in (True, False, "120", None):
        with pytest.raises(TypeError):
            gate.evaluate(perms_off, idle_seconds=bad_type)  # type: ignore[arg-type]
        with pytest.raises(TypeError):
            gate.evaluate(perms_off, min_idle_seconds_when_camera_off=bad_type)  # type: ignore[arg-type]

    # IEEE-754 negative zero (-0.0) is accepted and pauses open-compute cleanly
    neg_zero_res = gate.evaluate(perms_off, idle_seconds=-0.0)
    assert neg_zero_res["should_pause_open_compute"] is True
    assert main(["open-compute-gate", "--idle-seconds", "-0.0"]) == 0
    cli_out = json.loads(capsys.readouterr().out)
    assert cli_out["should_pause_open_compute"] is True


def test_cli_open_compute_gate_rejects_invalid_idle_seconds():
    for bad_arg in ("nan", "NaN", "inf", "-inf", "-1", "-0.1", "abc"):
        with pytest.raises(SystemExit) as exc:
            main(["open-compute-gate", "--idle-seconds", bad_arg])
        assert exc.value.code == 2


def test_camera_and_microphone_sensors_validate_adapter_outputs():
    cam_perms = SensationPermissions(camera=True)

    with pytest.raises(ValueError, match="3-tuple"):
        CameraPresenceSensor(detector=lambda: [True, 1, 0.9]).check_presence(cam_perms)  # type: ignore[return-value]
    with pytest.raises(ValueError, match="3-tuple"):
        CameraPresenceSensor(detector=lambda: (True, 1)).check_presence(cam_perms)  # type: ignore[return-value]
    with pytest.raises(TypeError):
        CameraPresenceSensor(detector=lambda: ("yes", 1, 0.9)).check_presence(cam_perms)  # type: ignore[return-value]
    with pytest.raises(ValueError):
        CameraPresenceSensor(detector=lambda: (True, -1, 0.9)).check_presence(cam_perms)
    with pytest.raises(ValueError):
        CameraPresenceSensor(detector=lambda: (True, True, 0.9)).check_presence(cam_perms)
    with pytest.raises(ValueError):
        CameraPresenceSensor(detector=lambda: (True, 1, float("nan"))).check_presence(cam_perms)
    with pytest.raises(ValueError):
        CameraPresenceSensor(detector=lambda: (True, 1, 10**400)).check_presence(cam_perms)
    with pytest.raises(ValueError):
        CameraPresenceSensor(detector=lambda: (True, 1, 1.01)).check_presence(cam_perms)
    with pytest.raises(ValueError):
        CameraPresenceSensor(detector=lambda: (True, 1, -0.01)).check_presence(cam_perms)
    with pytest.raises(ValueError, match="Contradictory detector result"):
        CameraPresenceSensor(detector=lambda: (False, 1, 0.95)).check_presence(cam_perms)

    obs_zero = CameraPresenceSensor(detector=lambda: (False, 0, -0.0)).check_presence(cam_perms)
    assert math.copysign(1.0, obs_zero.confidence) == 1.0

    mic_perms = SensationPermissions(microphone=True)
    with pytest.raises(ValueError, match="2-tuple"):
        MicrophoneAmbientSensor(sampler=lambda: [35.0, False]).sample_ambient(mic_perms)  # type: ignore[return-value]
    with pytest.raises(ValueError, match="2-tuple"):
        MicrophoneAmbientSensor(sampler=lambda: (35.0,)).sample_ambient(mic_perms)  # type: ignore[return-value]
    with pytest.raises(ValueError):
        MicrophoneAmbientSensor(sampler=lambda: (float("nan"), False)).sample_ambient(mic_perms)
    with pytest.raises(ValueError):
        MicrophoneAmbientSensor(sampler=lambda: (float("inf"), False)).sample_ambient(mic_perms)
    with pytest.raises(ValueError):
        MicrophoneAmbientSensor(sampler=lambda: (float("-inf"), False)).sample_ambient(mic_perms)
    with pytest.raises(ValueError):
        MicrophoneAmbientSensor(sampler=lambda: (10**400, False)).sample_ambient(mic_perms)
    with pytest.raises(TypeError):
        MicrophoneAmbientSensor(sampler=lambda: (True, False)).sample_ambient(mic_perms)
    with pytest.raises(TypeError):
        MicrophoneAmbientSensor(sampler=lambda: (40.0, "false")).sample_ambient(mic_perms)  # type: ignore[return-value]

    amb_zero = MicrophoneAmbientSensor(sampler=lambda: (-0.001, False)).sample_ambient(mic_perms)
    assert math.copysign(1.0, amb_zero.ambient_db) == 1.0


def test_cli_presence_help_and_fail_closed(capsys):
    with pytest.raises(PermissionError, match="camera=False"):
        main(["presence"])

    assert main(["presence", "--allow-camera"]) == 0
    pres_out = json.loads(capsys.readouterr().out)
    assert pres_out["user_present_at_pc"] is True
    assert pres_out["zero_egress_ram_only"] is True
    assert pres_out["source"] == "local_ram_presence_probe"

    with pytest.raises(SystemExit) as exc:
        main(["--help"])
    assert exc.value.code == 0
    help_text = capsys.readouterr().out
    for subcmd in ("status", "presence", "open-compute-gate"):
        assert subcmd in help_text


def test_microphone_exact_threshold_boundaries_and_empty_set_permissions():
    perms = SensationPermissions(microphone=True)
    assert MicrophoneAmbientSensor(sampler=lambda: (40.0, False)).sample_ambient(perms).noise_floor_state == "moderate"
    assert MicrophoneAmbientSensor(sampler=lambda: (65.0, False)).sample_ambient(perms).noise_floor_state == "loud"

    hub = SensationHub(permissions=SensationPermissions(camera=True, microphone=False, sound_output=False))
    returned = hub.set_permissions()
    assert returned.camera is True
    assert returned.microphone is False
    assert returned.sound_output is False
