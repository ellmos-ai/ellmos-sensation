# TODO: ellmos-sensation

**Audit Date:** 2026-11-18
**Auditor:** AI Security & Dependency Audit (`ellmos-ai`)
**Target Repo:** `ellmos-ai/ellmos-sensation`
**Version:** `0.1.0` (`development` / `public`)

---

## OPEN ROADMAP & OPERATIONS

- [ ] **Optional hardware camera presence adapter:** Document and test an optional pluggable `detector=` adapter (e.g., local OpenCV / MediaPipe behind an optional extra) without introducing mandatory runtime dependencies.
- [ ] **Optional microphone ambient RMS/VAD sampler:** Add an optional `sampler=` reference adapter and verify privacy/permission prompts against real audio backends.
- [ ] **`open-compute` integration smoke:** Verify end-to-end `OpenComputePresenceGate.evaluate()` integration inside `open-compute` desktop automation loops.

---

## COMPLETED HYGIENE & SECURITY HARDENING (2026-11-16 — 2026-11-18)

- [x] **Runtime fail-closed gate & permission hardening (2026-11-18):** Blocked `NaN`/`±Inf`/negative float bypasses in `OpenComputePresenceGate.evaluate()` and `--idle-seconds` CLI (`CWE-20`), enforced strict `bool` typing and atomic field whitelist in `SensationPermissions` / `SensationHub.set_permissions()` (`CWE-704`), validated `detector=`/`sampler=` outputs, and enforced `allow_nan=False` JSON output.
- [x] **PEP 639 build fix, Level-1 SBOM & Dependabot (2026-11-18):** Removed conflicting `License :: OSI Approved :: MIT License` classifier (`setuptools>=77` PEP 639 compatibility), added `THIRD_PARTY_LICENSES.md` (`license-files`), and added `.github/dependabot.yml` (`pip` & `github-actions`).
- [x] **GitHub CI workflow (2026-11-18):** Added minimal-privilege `.github/workflows/ci.yml` (`permissions: contents: read`) running `pytest`, `ruff check`, `compileall`, `pip check`, and wheel/sdist build verification across Python 3.10–3.13 (Ubuntu & Windows).
- [x] Hardened `.gitignore` with `final_gate_check.py` minimum entries plus SSH key wildcards (`id_rsa*`, `id_ed25519*`, `id_ecdsa*`, `id_dsa*`), certificate/token/secret globs, `MARKETING-LOG*`, `CONFLICT_REVIEW_LOG*`, and multi-host conflict patterns.
- [x] Synchronized `ellmos-module.v2.json` to full `ellmos.module.v2` schema (`category: "tools"`, `kind: "tool"`, `visibility: "public"`, `source_of_truth: git-repository`, `provides`, `surfaces`, `boundaries`) matching the module catalog.
- [x] Added PEP 561 marker `src/ellmos_sensation/py.typed`, `"Typing :: Typed"` classifier, PEP 639 `license-files`, and `[project.urls]` in `pyproject.toml`.
- [x] Created bilingual `SECURITY.md` (EN/DE, GitHub Private Vulnerability Reporting, `48h`/`5d`/`30d` SLAs) and `CHANGELOG.md`.
- [x] Added security, metadata/contract, and sensor/CLI edge-case tests in `tests/test_sensation_hub.py` and `tests/test_metadata.py` (`20` tests).
- [x] **Path-A Repository Hygiene & Cross-Platform CI (2026-11-24):** Added `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, `.github/ISSUE_TEMPLATE/{bug_report.md,feature_request.md}`, `MANIFEST.in`, PEP 621 `keywords` & `Contributing` URL, cross-platform `ci.yml` (`ubuntu`/`windows`/`macos`, Python `3.10`–`3.13`, `concurrency`, `ruff format --check`, sdist/wheel verification), `SECURITY.md` non-sensitive PVR-disabled fallback, `README.md`/`README_de.md` governance & test links, and privacy-gate cleanup in `tests/test_metadata.py`.

---

## STATUS

| Category | Status | Notes |
|---|---|---|
| Secrets | :green_circle: | Verified clean via `final_gate_check.py` (no live secrets tracked) |
| Private Data (PII) | :green_circle: | Verified clean via `final_gate_check.py` (0 PII warnings) |
| .gitignore | :green_circle: | Contains `__pycache__/`, `*.pyc`, `.env`, `*.db`, `.venv/`, `.idea/`, `.vscode/`, `data/`, SSH/key/token/secret & lock globs |
| Language (English) | :green_circle: | Bilingual `README.md` (EN) + `README_de.md` (DE) |
| BACH Internals | :green_circle: | None present |
| Database Files | :green_circle: | No `.db` or `.sqlite` files tracked (`state.ownership: "none"`) |
| README.md | :green_circle: | Present with permission model, API examples, CLI usage, and placeholder boundary |
| LICENSE | :green_circle: | MIT (`LICENSE` & `THIRD_PARTY_LICENSES.md` declared via PEP 639 `license-files`) |
| SECURITY.md | :green_circle: | Bilingual EN/DE policy with GitHub Private Vulnerability Reporting, fail-closed invariants & 48h/5d/30d SLAs |
| **Overall** | **READY** | Gate check ready (`10 PASS, 0 FAIL, 0 WARN`) |

**Audit Date:** 2026-11-18
**Gate Check Exit Code:** `0`
