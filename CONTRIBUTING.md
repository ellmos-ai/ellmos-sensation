# Beitragsrichtlinie / Contributing Guide

## Deutsch

Vielen Dank für Ihr Interesse, zu `ellmos-sensation` beizutragen!

### Wie Sie beitragen können

1. **Bug melden:** Erstellen Sie ein Issue mit dem Label `bug` über die Vorlage `Bug Report / Fehlerbericht`.
2. **Feature vorschlagen:** Erstellen Sie ein Issue mit dem Label `enhancement` über die Vorlage `Feature Request / Funktionswunsch`.
3. **Code oder Doku beitragen:** Erstellen Sie einen Pull Request gegen `main`.

### Entwicklung & lokale Prüfung

```bash
pip install -e ".[dev]"
python -m pytest -v
python -m ruff check .
python -m ruff format --check .
python -m compileall -q src tests
```

### Pull Requests

1. Forken Sie das Repository.
2. Erstellen Sie einen Branch: `git checkout -b feature/mein-feature`
3. Stellen Sie sicher, dass Fail-Closed-Berechtigungen (`camera=False`, `microphone=False`), strikte `bool`-/`NaN`-Validierungen und Zero-Egress-Grenzen gewahrt bleiben.
4. Committen Sie Ihre Änderungen und eröffnen Sie einen Pull Request.

### Richtlinien

- Python >= 3.10, UTF-8-Encoding, Ruff-Formatierung (Zeilenlänge 120)
- Keine externen Laufzeitpflichtabhängigkeiten in `[project].dependencies`
- Keine hartkodierten lokalen Pfade, Credentials oder Laufzeitdatenbanken
- Einhalten des [Verhaltenskodex](CODE_OF_CONDUCT.md)

---

## English

Thank you for your interest in contributing to `ellmos-sensation`!

### How to Contribute

1. **Report bugs:** Open an issue with the `bug` label using the `Bug Report / Fehlerbericht` template.
2. **Suggest features:** Open an issue with the `enhancement` label using the `Feature Request / Funktionswunsch` template.
3. **Contribute code or docs:** Open a Pull Request targeting `main`.

### Development & Local Verification

```bash
pip install -e ".[dev]"
python -m pytest -v
python -m ruff check .
python -m ruff format --check .
python -m compileall -q src tests
```

### Pull Requests

1. Fork the repository.
2. Create a branch: `git checkout -b feature/my-feature`
3. Preserve fail-closed permissions (`camera=False`, `microphone=False`), strict `bool`/`NaN` validation, and zero-egress boundaries.
4. Commit your changes and open a Pull Request.

### Guidelines

- Python >= 3.10, UTF-8 encoding, Ruff formatting (line length 120)
- Zero mandatory external runtime dependencies in `[project].dependencies`
- No hardcoded local paths, credentials, or runtime databases
- Follow the [Code of Conduct](CODE_OF_CONDUCT.md)
