# Third-Party Licenses & Level-1 SBOM (`ellmos-sensation`)

- **Package:** `ellmos-sensation` (`0.1.0`)
- **Project License:** `MIT` (see [LICENSE](LICENSE))
- **Repository:** <https://github.com/ellmos-ai/ellmos-sensation>
- **Re-Audit:** `2026-11-18`

---

## 1. Direct & Transitive Runtime Dependencies (`[project.dependencies]`)

`ellmos-sensation` has **zero external runtime dependencies** (`dependencies = []` in `pyproject.toml`).

At runtime, the package uses exclusively modules from the **Python Standard Library** (`>=3.10`, licensed under `PSF-2.0`):
`argparse`, `collections.abc`, `dataclasses`, `datetime`, `io`, `json`, `math`, `struct`, `typing`, and `wave`.

---

## 2. Build & Development Dependencies (`[build-system]` & `[project.optional-dependencies].dev`)

Build and development dependencies are used exclusively for packaging, testing, and static analysis; none are required or bundled at runtime:

| Package | Version Constraint | Audited Version | SPDX License | Upstream | Purpose |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `setuptools` | `>=77` | `82.0.1` | `MIT` | <https://github.com/pypa/setuptools> | PEP 517 / PEP 639 build backend (`setuptools.build_meta`). |
| `pytest` | `>=8.0` | `9.2.0` | `MIT` | <https://github.com/pytest-dev/pytest> | Automated unit, boundary, and metadata contract test runner. |
| `ruff` | `>=0.8` | `0.16.8` | `MIT` | <https://github.com/astral-sh/ruff> | Static Python linter and code hygiene checker. |
| `build` | `>=1.2` | `1.5.0` | `MIT` | <https://github.com/pypa/build> | Isolated wheel and sdist verification builder. |
| `tomli` | `>=2.0; python_version < '3.11'` | `>=2.0` (`python_version < '3.11'` only) | `MIT` | <https://github.com/hukkin/tomli> | TOML metadata test parser fallback on Python 3.10 (`tomllib` stdlib used on `>=3.11`). |

---

## 3. Supply-Chain & Security Governance Invariants

| Invariant | Status | Verification & Policy |
| :--- | :--- | :--- |
| `INV-LIC-01` (Project License & PEP 639) | `PASS` | `MIT` SPDX expression in `pyproject.toml` (`license = "MIT"`, `license-files = ["LICENSE", "THIRD_PARTY_LICENSES.md"]`, zero deprecated `License ::` classifiers). |
| `INV-SBOM-02` (Zero-Runtime-Dependency Surface) | `PASS` | `dependencies = []` (`0` external runtime requirements; CI verifies `python -m pip check` in clean environments); automated weekly monitoring via `.github/dependabot.yml` (`pip` & `github-actions`). |
| `INV-E08-03` (Copyleft Boundary) | `PASS` | `100%` permissive (`MIT` / `PSF-2.0`); `0%` AGPL/GPL/LGPL dependencies across runtime, build, and test scopes. |
| `INV-SAFE-04` (Fail-Closed Gate & Strict Permissions) | `PASS` | `SensationPermissions` (`camera=False`, `microphone=False` default) rejects non-`bool` truthy coercion (`CWE-704`) and method overwrite; `OpenComputePresenceGate` rejects `NaN`/`Inf`/negative idle values (`CWE-20`); `boundaries.network = "none"`. |
| `INV-SLA-09` (Acknowledgement & Triage SLA) | `PASS` | **48 hours** acknowledgement (`48 Stunden` Eingangsbestätigung) and **5 business days** initial triage (`5 Werktage` Ersteinschätzung) via GitHub Private Vulnerability Reporting in `SECURITY.md`. |
| `INV-SLA-10` (Remediation SLA) | `PASS` | Binding **30 calendar days** remediation SLA (`30 Kalendertage` Behebungszusage) for confirmed vulnerabilities in `SECURITY.md`. |
