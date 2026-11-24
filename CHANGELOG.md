# Changelog

All notable changes to `ellmos-sensation` will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Bilingual community governance files (`CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`) and `.github/ISSUE_TEMPLATE/{bug_report.md,feature_request.md}` (DE/EN).
- `MANIFEST.in` source-distribution manifest ensuring deterministic packaging of docs, `ellmos-module.v2.json`, `py.typed`, assets, and tests.
- PEP 621 `keywords` and `Contributing` URL in `pyproject.toml` (version `0.1.0` unchanged).
- Expanded contract and CLI boundary tests in `tests/test_metadata.py` and `tests/test_sensation_hub.py`.

### Changed
- Hardened `.github/workflows/ci.yml` with `concurrency` cancellation, `timeout-minutes: 10`, cross-platform matrix across `ubuntu-latest` (3.10–3.13), `windows-latest` (3.12–3.13), and `macos-latest` (3.12–3.13), `pip install --no-build-isolation --dry-run .`, sdist verification, `git diff --check`, and `ruff format --check .`.
- Updated `SECURITY.md` with an explicit non-sensitive coordination fallback when GitHub Private Vulnerability Reporting is disabled on the repository.
- Updated `README.md` and `README_de.md` to reference both `tests/test_sensation_hub.py` and `tests/test_metadata.py` and link governance/license documents.
- Added CLI option `--help` descriptions for `open-compute-gate` and aligned source formatting with `ruff format`.

### Security
- **Fail-closed `OpenComputePresenceGate` & CLI validation (`CWE-20`):** `OpenComputePresenceGate.evaluate()` and `ellmos-sensation open-compute-gate --idle-seconds` now reject `NaN`, `±Infinity`, boolean, and negative idle-time values instead of silently evaluating `NaN < threshold` as `False`. CLI output enforces strict RFC-8259 JSON (`allow_nan=False`).
- **Strict boolean permission enforcement (`CWE-704`):** `SensationPermissions` and `SensationHub.set_permissions()` now enforce strict `bool` values (rejecting truthy strings such as `"false"` or `"0"` and non-boolean types with `TypeError`), restrict `set_permissions()` atomically to the declared permission fields (`camera`, `microphone`, `sound_output`), and guard sensor entrypoints against post-init attribute tampering.
- **Sensor adapter output validation:** `CameraPresenceSensor.check_presence()` and `MicrophoneAmbientSensor.sample_ambient()` now validate custom `detector=` and `sampler=` return types, finite numeric bounds (`confidence` in `[0.0, 1.0]`, finite `ambient_db`), non-negative integer `person_count`, and non-contradictory presence states.

### Added
- Level-1 SBOM `THIRD_PARTY_LICENSES.md` documenting zero external runtime dependencies, audited build/dev tool licenses, and security governance invariants (`INV-SLA-09` & `INV-SLA-10`).
- Minimal-privilege GitHub Actions workflow `.github/workflows/ci.yml` (`permissions: contents: read`, Python 3.10–3.13 on Ubuntu and Python 3.12 on Windows) and weekly `.github/dependabot.yml` (`pip` & `github-actions`).
- Standardized `TODO.md` with release-gate `## STATUS` table (`10/10 PASS` on `final_gate_check.py`).
- Bilingual `SECURITY.md` (EN/DE) documenting fail-closed permissions, zero-egress RAM-only boundaries, GitHub Private Vulnerability Reporting, and `48h`/`5d`/`30d` SLAs (`INV-SLA-09` & `INV-SLA-10`).
- PEP 561 typing marker (`src/ellmos_sensation/py.typed`), `"Typing :: Typed"` classifier, PEP 639 `license-files = ["LICENSE", "THIRD_PARTY_LICENSES.md"]`, and `[project.urls]` in `pyproject.toml`.
- Expanded security, contract, and edge-case test suite in `tests/test_sensation_hub.py` and `tests/test_metadata.py` (`17` tests).

### Fixed
- Removed deprecated `"License :: OSI Approved :: MIT License"` classifier from `pyproject.toml` to resolve PEP 639 `setuptools` `InvalidConfigError` during wheel/sdist builds.

### Changed
- Hardened `.gitignore` with complete Python, test/lint cache, environment/secret, SSH key wildcard (`id_rsa*`, `id_ed25519*`, `id_ecdsa*`, `id_dsa*`), certificate/token/secret, database, IDE, `MARKETING-LOG*`, `CONFLICT_REVIEW_LOG*`, multi-host conflict, and fleet lock exclusion rules.
- Synchronized `ellmos-module.v2.json` to the canonical `ellmos.module.v2` schema (`category: "tools"`, `kind: "tool"`, `status: "development"`, `visibility: "public"`, `provides`, `surfaces`, `boundaries`, `source_of_truth`), keeping version `0.1.0` unchanged.

## [0.1.0] - 2026-11-02

### Added
- Initial public module release of `ellmos-sensation` (`SensationPermissions`, `CameraPresenceSensor`, `MicrophoneAmbientSensor`, `SoundSynthesizer`, `OpenComputePresenceGate`, `SensationHub`, and `ellmos-sensation` CLI).
- Bilingual documentation (`README.md`, `README_de.md`), `LICENSE` (MIT), and repository banner (`assets/banner.svg`, `assets/banner.png`).
