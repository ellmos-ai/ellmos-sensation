"""Tests for ellmos-sensation permission gates, sensors, and Open-Compute presence gate."""

from __future__ import annotations

import json
import pytest

from ellmos_sensation import (
    CameraPresenceSensor,
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
