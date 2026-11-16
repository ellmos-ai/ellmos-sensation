# TODO: ellmos-sensation

**Audit Date:** 2026-11-16
**Auditor:** AI Modules Care (`ellmos-ai`)
**Target Repo:** `ellmos-ai/ellmos-sensation`
**Version:** `0.1.0` (`development` / `public`)

---

## OPEN ROADMAP & OPERATIONS

- [ ] **Optional hardware camera presence adapter:** Document and test an optional pluggable `detector=` adapter (e.g., local OpenCV / MediaPipe behind an optional extra) without introducing mandatory runtime dependencies.
- [ ] **Optional microphone ambient RMS/VAD sampler:** Add an optional `sampler=` reference adapter and verify privacy/permission prompts against real audio backends.
- [ ] **`open-compute` integration smoke:** Verify end-to-end `OpenComputePresenceGate.evaluate()` integration inside `open-compute` desktop automation loops.
- [ ] **GitHub CI workflow:** Add a minimal-privilege `.github/workflows/ci.yml` (`permissions: contents: read`) running `pytest`, `ruff check`, and `compileall` across Python 3.10–3.13.

---

## COMPLETED HYGIENE (2026-11-16)

- [x] Hardened `.gitignore` with `final_gate_check.py` minimum entries (`*.pyc`, `.env`, `*.db`, `.venv/`, `.idea/`, `.vscode/`, `data/`, `LOCK*.txt`, secret/cache patterns).
- [x] Synchronized `ellmos-module.v2.json` to full `ellmos.module.v2` schema (`category: "tools"`, `kind: "tool"`, `visibility: "public"`, `source_of_truth: git-repository`, `provides`, `surfaces`, `boundaries`) matching the module catalog.
- [x] Added PEP 561 marker `src/ellmos_sensation/py.typed`, `"Typing :: Typed"` classifier, PEP 639 `license-files = ["LICENSE"]`, and `[project.urls]` in `pyproject.toml`.
- [x] Created bilingual `SECURITY.md` (EN/DE, GitHub Private Vulnerability Reporting, `48h`/`5d`/`30d` SLAs) and `CHANGELOG.md`.
- [x] Added metadata/contract and sensor/CLI edge-case tests in `tests/test_metadata.py`.

---

## STATUS

| Category | Status | Notes |
|---|---|---|
| Secrets | :green_circle: | Verified clean via `final_gate_check.py` (no live secrets tracked) |
| Private Data (PII) | :green_circle: | Verified clean via `final_gate_check.py` (0 PII warnings) |
| .gitignore | :green_circle: | Contains `__pycache__/`, `*.pyc`, `*.py[cod]`, `.env`, `*.db`, `.venv/`, `.idea/`, `.vscode/`, `data/`, `LOCK*.txt` |
| Language (English) | :green_circle: | Bilingual `README.md` (EN) + `README_de.md` (DE) |
| BACH Internals | :green_circle: | None present |
| Database Files | :green_circle: | No `.db` or `.sqlite` files tracked (`state.ownership: "none"`) |
| README.md | :green_circle: | Present with permission model, API examples, CLI usage, and placeholder boundary |
| LICENSE | :green_circle: | MIT (`LICENSE` present and declared via PEP 639 `license-files`) |
| SECURITY.md | :green_circle: | Bilingual EN/DE policy with GitHub Private Vulnerability Reporting & 48h/5d/30d SLAs |
| **Overall** | **READY** | Gate check ready (`10 PASS, 0 FAIL, 0 WARN`) |

**Audit Date:** 2026-11-16
**Gate Check Exit Code:** `0`
