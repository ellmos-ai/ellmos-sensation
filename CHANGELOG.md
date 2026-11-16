# Changelog

All notable changes to `ellmos-sensation` will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Standardized `TODO.md` with release-gate `## STATUS` table (`10/10 PASS` on `final_gate_check.py`).
- Bilingual `SECURITY.md` (EN/DE) documenting fail-closed permissions, zero-egress RAM-only boundaries, GitHub Private Vulnerability Reporting, and `48h`/`5d`/`30d` SLAs (`INV-SLA-09` & `INV-SLA-10`).
- PEP 561 typing marker (`src/ellmos_sensation/py.typed`), `"Typing :: Typed"` classifier, PEP 639 `license-files = ["LICENSE"]`, and `[project.urls]` in `pyproject.toml`.
- Contract and edge-case tests in `tests/test_metadata.py` covering version parity, v2 manifest schema conformance, PEP 561/639 metadata, `.gitignore` hygiene, bilingual docs, sensor thresholds, and CLI boundaries.

### Changed
- Hardened `.gitignore` with complete Python, test/lint cache, environment/secret, database, IDE, and multi-agent lock exclusion rules (`*.pyc`, `.env*`, `*.db`, `.venv/`, `.idea/`, `.vscode/`, `data/`, `LOCK*.txt`).
- Synchronized `ellmos-module.v2.json` to the canonical `ellmos.module.v2` schema (`category: "tools"`, `kind: "tool"`, `status: "development"`, `visibility: "public"`, `provides`, `surfaces`, `boundaries`, `source_of_truth`), keeping version `0.1.0` unchanged.

## [0.1.0] - 2026-11-02

### Added
- Initial public module release of `ellmos-sensation` (`SensationPermissions`, `CameraPresenceSensor`, `MicrophoneAmbientSensor`, `SoundSynthesizer`, `OpenComputePresenceGate`, `SensationHub`, and `ellmos-sensation` CLI).
- Bilingual documentation (`README.md`, `README_de.md`), `LICENSE` (MIT), and repository banner (`assets/banner.svg`, `assets/banner.png`).
