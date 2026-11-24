"""Contract, metadata, and edge-case tests for ellmos-sensation."""

from __future__ import annotations

import io
import json
import re
import sys
import wave
from pathlib import Path

import pytest

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib

import ellmos_sensation
from ellmos_sensation import (
    MicrophoneAmbientSensor,
    OpenComputePresenceGate,
    SensationHub,
    SensationPermissions,
    SoundSynthesizer,
)
from ellmos_sensation.cli import main

ROOT = Path(__file__).resolve().parent.parent


def test_version_parity_and_pyproject_metadata():
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    manifest = json.loads((ROOT / "ellmos-module.v2.json").read_text(encoding="utf-8"))

    project = pyproject["project"]
    assert pyproject["build-system"]["requires"] == ["setuptools>=77"]
    assert project["name"] == "ellmos-sensation"
    assert project["version"] == ellmos_sensation.__version__ == manifest["version"] == "0.1.0"
    assert project["license"] == "MIT"
    assert project["license-files"] == ["LICENSE", "THIRD_PARTY_LICENSES.md"]
    assert all(not c.startswith("License ::") for c in project["classifiers"])
    assert "Typing :: Typed" in project["classifiers"]
    assert "ellmos-sensation" in project["scripts"]
    assert len(project["keywords"]) >= 5
    assert "Contributing" in project["urls"]
    assert "Security" in project["urls"]
    assert "Third-Party Licenses" in project["urls"]

    pkg_data = pyproject["tool"]["setuptools"]["package-data"]
    assert "py.typed" in pkg_data["ellmos_sensation"]

    pytest_ini = pyproject["tool"]["pytest"]["ini_options"]
    assert "--basetemp" not in str(pytest_ini.get("addopts", ""))


def test_pep561_py_typed_and_required_release_files():
    assert (ROOT / "src" / "ellmos_sensation" / "py.typed").is_file()
    assert (ROOT / "LICENSE").is_file()
    assert (ROOT / "THIRD_PARTY_LICENSES.md").is_file()
    assert (ROOT / "CHANGELOG.md").is_file()

    security_text = (ROOT / "SECURITY.md").read_text(encoding="utf-8")
    assert "https://github.com/ellmos-ai/ellmos-sensation/security/advisories/new" in security_text
    assert "Private Vulnerability Reporting is disabled" in security_text
    assert "Private Vulnerability Reporting im Repository deaktiviert ist" in security_text
    assert "48 hours" in security_text and "48 Stunden" in security_text
    assert "5 business days" in security_text and "5 Werktagen" in security_text
    assert "30 calendar days" in security_text and "30 Kalendertagen" in security_text


def test_community_governance_and_packaging_manifest():
    coc = (ROOT / "CODE_OF_CONDUCT.md").read_text(encoding="utf-8")
    assert "## Deutsch" in coc and "## English" in coc
    assert "Contributor Covenant v2.1" in coc
    assert "SECURITY.md" in coc

    contrib = (ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")
    assert "## Deutsch" in contrib and "## English" in contrib
    assert "ruff format --check ." in contrib
    assert "pytest" in contrib

    bug_tpl = (ROOT / ".github" / "ISSUE_TEMPLATE" / "bug_report.md").read_text(encoding="utf-8")
    feat_tpl = (ROOT / ".github" / "ISSUE_TEMPLATE" / "feature_request.md").read_text(encoding="utf-8")
    assert "labels: bug" in bug_tpl
    assert "labels: enhancement" in feat_tpl

    for doc in (coc, contrib, bug_tpl, feat_tpl):
        assert "geiger.sh" not in doc.lower()

    manifest_in = (ROOT / "MANIFEST.in").read_text(encoding="utf-8")
    for required in ("include ellmos-module.v2.json", "include SECURITY.md", "recursive-include src *.py py.typed"):
        assert required in manifest_in


def test_sbom_ci_dependabot_and_security_hygiene_contracts():
    sbom = (ROOT / "THIRD_PARTY_LICENSES.md").read_text(encoding="utf-8")
    for token in ("ellmos-sensation", "0.1.0", "MIT", "INV-SLA-09", "INV-SLA-10", "2026-11-18"):
        assert token in sbom

    ci_path = ROOT / ".github" / "workflows" / "ci.yml"
    assert ci_path.is_file()
    ci_text = ci_path.read_text(encoding="utf-8")
    assert "contents: read" in ci_text
    assert "concurrency:" in ci_text
    assert "timeout-minutes:" in ci_text
    assert 'PYTHONUTF8: "1"' in ci_text
    for os_name in ("ubuntu-latest", "windows-latest", "macos-latest"):
        assert os_name in ci_text
    for py_ver in ('"3.10"', '"3.11"', '"3.12"', '"3.13"'):
        assert py_ver in ci_text
    assert "pip install --no-build-isolation --dry-run ." in ci_text
    assert "ruff check" in ci_text
    assert "ruff format --check" in ci_text
    assert "git diff --check" in ci_text
    assert "tarfile" in ci_text
    assert "pytest" in ci_text
    assert "compileall" in ci_text

    dep_path = ROOT / ".github" / "dependabot.yml"
    assert dep_path.is_file()
    dep_text = dep_path.read_text(encoding="utf-8")
    assert 'package-ecosystem: "pip"' in dep_text
    assert 'package-ecosystem: "github-actions"' in dep_text


def test_module_manifest_v2_schema_compliance():
    manifest = json.loads((ROOT / "ellmos-module.v2.json").read_text(encoding="utf-8"))
    assert manifest["schema"] == "ellmos.module.v2"
    assert manifest["id"] == "ellmos-sensation"
    assert manifest["category"] == "tools"
    assert manifest["kind"] == "tool"
    assert manifest["status"] == "development"
    assert manifest["visibility"] == "public"
    assert manifest["surfaces"] == ["library", "cli"]
    assert manifest["boundaries"]["network"] == "none"
    assert manifest["boundaries"]["data"] == "user-local"
    assert manifest["source_of_truth"]["type"] == "git-repository"
    assert manifest["source_of_truth"]["repository"] == "https://github.com/ellmos-ai/ellmos-sensation"


def test_gitignore_and_todo_status_contract():
    gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
    for entry in (
        "__pycache__",
        "*.pyc",
        ".env",
        "*.db",
        ".venv",
        ".idea",
        ".vscode",
        "data",
        "LOCK*.txt",
        "id_rsa*",
        "id_ed25519*",
        "id_ecdsa*",
        "id_dsa*",
        "*.csr",
        "*.token",
        "*.secret",
        "*secret*.json",
        "*token*.json",
        "MARKETING-LOG*",
        "CONFLICT_REVIEW_LOG*",
    ):
        assert entry in gitignore
    for host_prefix in ("WORKSTATION", "ASUS", "IDEAPAD"):
        host_suffix = "LG" if host_prefix == "WORKSTATION" else "GEI"
        assert f"*-{host_prefix}-{host_suffix}*" in gitignore

    todo = (ROOT / "TODO.md").read_text(encoding="utf-8")
    assert "## STATUS" in todo
    assert "| Category" in todo
    assert "**READY**" in todo


def test_bilingual_readme_and_zero_personal_paths():
    readme_en = (ROOT / "README.md").read_text(encoding="utf-8")
    readme_de = (ROOT / "README_de.md").read_text(encoding="utf-8")
    assert "assets/banner.svg" in readme_en
    assert "assets/banner.svg" in readme_de
    assert (ROOT / "assets" / "banner.svg").is_file()

    for readme_text in (readme_en, readme_de):
        assert "tests/test_sensation_hub.py" in readme_text
        assert "tests/test_metadata.py" in readme_text
        for linked_file in (
            "LICENSE",
            "SECURITY.md",
            "CONTRIBUTING.md",
            "CODE_OF_CONDUCT.md",
            "CHANGELOG.md",
            "THIRD_PARTY_LICENSES.md",
        ):
            assert f"({linked_file})" in readme_text
            assert (ROOT / linked_file).is_file()
        for target in re.findall(r"\[[^\]]+\]\(([^)#]+)\)", readme_text):
            if "://" in target:
                continue
            assert (ROOT / target).exists(), f"Broken local link in README: {target}"

    user_token = "luk" + "as"
    personal_re = re.compile(
        rf"C:[\\/]+Users[\\/]+(?:{user_token}|User)(?=[\\/]|$)|/home/{user_token}|/Users/{user_token}",
        re.IGNORECASE,
    )
    for path in list((ROOT / "src").rglob("*.py")) + list((ROOT / "tests").rglob("*.py")):
        content = path.read_text(encoding="utf-8")
        assert not personal_re.search(content), f"Personal path found in {path}"


def test_microphone_thresholds_and_synthesizer_presets():
    perms = SensationPermissions(microphone=True, sound_output=True)
    quiet = MicrophoneAmbientSensor(sampler=lambda: (25.0, False)).sample_ambient(perms)
    moderate = MicrophoneAmbientSensor(sampler=lambda: (45.256, True)).sample_ambient(perms)
    loud = MicrophoneAmbientSensor(sampler=lambda: (72.0, True)).sample_ambient(perms)

    assert quiet.noise_floor_state == "quiet"
    assert moderate.noise_floor_state == "moderate"
    assert moderate.ambient_db == 45.26
    assert moderate.speech_detected is True
    assert loud.noise_floor_state == "loud"

    synth = SoundSynthesizer()
    for cue in SoundSynthesizer.PRESETS:
        wav_bytes = synth.synthesize_cue_wav(cue, perms)
        with wave.open(io.BytesIO(wav_bytes), "rb") as wf:
            assert wf.getnchannels() == 1
            assert wf.getsampwidth() == 2
            assert wf.getframerate() == 16_000
            assert wf.getnframes() > 0

    with pytest.raises(ValueError, match="Unknown sound cue"):
        synth.synthesize_cue_wav("nonexistent", perms)


def test_hub_unknown_permission_and_gate_idle_boundary(capsys):
    hub = SensationHub()
    with pytest.raises(ValueError, match="Unknown permission flag"):
        hub.set_permissions(gps=True)

    gate = OpenComputePresenceGate()
    assert gate.evaluate(SensationPermissions(camera=False), idle_seconds=119.9)["should_pause_open_compute"] is True
    assert gate.evaluate(SensationPermissions(camera=False), idle_seconds=120.0)["should_pause_open_compute"] is False

    assert main(["open-compute-gate", "--idle-seconds", "300"]) == 0
    out = json.loads(capsys.readouterr().out)
    assert out["camera_checked"] is False
    assert out["should_pause_open_compute"] is False
    assert out["reason"] == "idle_timeout_elapsed"
