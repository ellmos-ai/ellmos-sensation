# Security Policy / Sicherheitsrichtlinie

---

## English

### Scope & Threat Model

`ellmos-sensation` is a zero-dependency Python package providing permission-gated device sensing abstractions (`CameraPresenceSensor`, `MicrophoneAmbientSensor`), acoustic earcon synthesis (`SoundSynthesizer`), and the `OpenComputePresenceGate` guard for local AI runtimes (`ELLMOS`, `BACH`, `Open Ocean`):

- **Fail-closed permissions & strict boolean typing (`CWE-704`):** `SensationPermissions` sets `camera=False` and `microphone=False` by default (`sound_output=True`), enforces strict `bool` validation (rejecting truthy strings such as `"false"` or `"0"` and non-boolean types with `TypeError`), and restricts `SensationHub.set_permissions()` atomically to the declared permission flags. Calling `CameraPresenceSensor.check_presence()` or `MicrophoneAmbientSensor.sample_ambient()` without explicit `True` permission raises `PermissionError`.
- **Fail-closed safety gate & adapter validation (`CWE-20`):** `OpenComputePresenceGate.evaluate()` and the `ellmos-sensation open-compute-gate` CLI reject `NaN`, `±Infinity`, boolean, and negative idle-time inputs instead of silently evaluating `NaN < threshold` as `False`. Custom `detector=` and `sampler=` outputs are validated for finite numeric bounds, non-negative integer counts, and non-contradictory presence states, and CLI output enforces strict RFC-8259 JSON (`allow_nan=False`).
- **Zero-egress RAM-only data model:** `PresenceObservation` carries `zero_egress_ram_only=True`, and the package makes zero network calls (`boundaries.network: "none"` in `ellmos-module.v2.json`). Note that `zero_egress_ram_only` is a data-model property — OS-level sandboxing or camera hardware permissions remain the host/caller responsibility.
- **Placeholder output boundary (`v0.1.0`):** Unless custom `detector=` or `sampler=` callables are injected, `CameraPresenceSensor` and `MicrophoneAmbientSensor` return deterministic placeholder values rather than reading physical hardware. Callers must not treat default placeholder outputs as live sensor measurements.
- **No external runtime dependencies & Level-1 SBOM:** Core runtime uses only the Python standard library (`argparse`, `collections.abc`, `dataclasses`, `datetime`, `io`, `json`, `math`, `struct`, `typing`, `wave`). Build/dev dependencies and governance invariants are documented in [THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md) and monitored weekly via Dependabot.

### Supported Versions

| Version | Supported |
|---------|-----------|
| `0.1.x` (`0.1.0`) | Yes (`main`) |
| `< 0.1.0` | No |

### Reporting a Vulnerability & Response SLAs (`INV-SLA-09` / `INV-SLA-10`)

Please **do not** report unpatched security vulnerabilities through public GitHub issues, pull requests, or discussions.

Report vulnerabilities privately via **GitHub Private Vulnerability Reporting**:
- **Advisory Portal:** <https://github.com/ellmos-ai/ellmos-sensation/security/advisories/new>

Include affected version, platform, minimal reproduction steps, and impact assessment. Never include live credentials or personal hardware captures in reports.

Our binding response and remediation targets (`INV-SLA-09` & `INV-SLA-10`):
- **Acknowledgement:** within **48 hours**
- **Initial triage & severity assessment:** within **5 business days**
- **Remediation SLA (patch or documented mitigation for confirmed vulnerabilities):** within **30 calendar days**

---

## Deutsch (Sicherheitsrichtlinie)

### Geltungsbereich & Bedrohungsmodell

`ellmos-sensation` ist ein abhängigkeitsfreies Python-Paket für berechtigungsgesteuerte Gerätesensorik-Abstraktionen (`CameraPresenceSensor`, `MicrophoneAmbientSensor`), akustische Hinweistöne (`SoundSynthesizer`) und das `OpenComputePresenceGate` für lokale KI-Laufzeitumgebungen (`ELLMOS`, `BACH`, `Open Ocean`):

- **Fail-Closed-Berechtigungen & strikte Bool-Prüfung (`CWE-704`):** `SensationPermissions` setzt standardmäßig `camera=False` und `microphone=False` (`sound_output=True`), erzwingt echte `bool`-Werte (weist nicht-boolesche Typen sowie Strings wie `"false"` oder `"0"` mit `TypeError` ab) und beschränkt `SensationHub.set_permissions()` atomar auf die deklarierten Berechtigungsfelder. Ein Aufruf von `CameraPresenceSensor.check_presence()` oder `MicrophoneAmbientSensor.sample_ambient()` ohne explizite Freigabe löst `PermissionError` aus.
- **Fail-Closed-Präsenz-Gate & Adapter-Validierung (`CWE-20`):** `OpenComputePresenceGate.evaluate()` und das CLI `ellmos-sensation open-compute-gate` weisen `NaN`, `±Infinity`, Bool-Werte und negative Leerlaufzeiten strikt ab, statt `NaN < Schwellenwert` stillschweigend als `False` auszuwerten. Rückgabewerte benutzerdefinierter `detector=`- und `sampler=`-Funktionen werden auf endliche Zahlenbereiche, nichtnegative Personenzähler und widerspruchsfreie Präsenzangaben geprüft; alle CLI-Ausgaben erzwingen striktes RFC-8259-JSON (`allow_nan=False`).
- **Zero-Egress-RAM-Only-Datenmodell:** `PresenceObservation` trägt `zero_egress_ram_only=True`, und das Paket führt keinerlei Netzwerkaufrufe aus (`boundaries.network: "none"` in `ellmos-module.v2.json`). Das Flag beschreibt die Paketarchitektur; Betriebssystem-Sandbox und Hardware-Zugriffsrechte liegen in der Verantwortung der aufrufenden Umgebung.
- **Platzhalter-Grenze (`v0.1.0`):** Ohne übergebene `detector=`- bzw. `sampler=`-Funktionen liefern `CameraPresenceSensor` und `MicrophoneAmbientSensor` feste Platzhalterwerte und lesen keine physische Hardware aus. Standardausgaben dürfen nicht als echte Live-Messung interpretiert werden.
- **Keine externen Laufzeitabhängigkeiten & Level-1-SBOM:** Die Laufzeit nutzt ausschließlich die Python-Standardbibliothek (`argparse`, `collections.abc`, `dataclasses`, `datetime`, `io`, `json`, `math`, `struct`, `typing`, `wave`). Build-/Entwicklungsabhängigkeiten und Sicherheitsinvarianten sind in [THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md) dokumentiert und werden wöchentlich über Dependabot überwacht.

### Unterstützte Versionen

| Version | Unterstützt |
|---------|-------------|
| `0.1.x` (`0.1.0`) | Ja (`main`) |
| `< 0.1.0` | Nein |

### Sicherheitslücken melden & Reaktionsfristen (`INV-SLA-09` / `INV-SLA-10`)

Bitte melden Sie ungepatchte Sicherheitslücken **niemals** über öffentliche GitHub-Issues, Pull-Requests oder Diskussionen.

Nutzen Sie ausschließlich die vertrauliche Meldung über **GitHub Private Vulnerability Reporting**:
- **Sicherheitsmeldung einreichen:** <https://github.com/ellmos-ai/ellmos-sensation/security/advisories/new>

Verbindliche Reaktions- und Behebungsziele (`INV-SLA-09` & `INV-SLA-10`):
- **Eingangsbestätigung:** innerhalb von **48 Stunden**
- **Ersteinschätzung & Schweregrad-Triage:** innerhalb von **5 Werktagen**
- **Behebungszusage (Patch oder dokumentierte Risikominderung für bestätigte Schwachstellen):** innerhalb von **30 Kalendertagen**
