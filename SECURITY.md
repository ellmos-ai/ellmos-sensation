# Security Policy / Sicherheitsrichtlinie

---

## English

### Scope & Threat Model

`ellmos-sensation` is a zero-dependency Python package providing permission-gated device sensing abstractions (`CameraPresenceSensor`, `MicrophoneAmbientSensor`), acoustic earcon synthesis (`SoundSynthesizer`), and the `OpenComputePresenceGate` guard for local AI runtimes (`ELLMOS`, `BACH`, `Open Ocean`):

- **Fail-closed permissions by default:** `SensationPermissions` sets `camera=False` and `microphone=False` by default (`sound_output=True`). Calling `CameraPresenceSensor.check_presence()` or `MicrophoneAmbientSensor.sample_ambient()` without explicit opt-in raises `PermissionError`.
- **Zero-egress RAM-only data model:** `PresenceObservation` carries `zero_egress_ram_only=True`, and the package makes zero network calls (`boundaries.network: "none"` in `ellmos-module.v2.json`). Note that `zero_egress_ram_only` is a data-model property — OS-level sandboxing or camera hardware permissions remain the host/caller responsibility.
- **Placeholder output boundary (`v0.1.0`):** Unless custom `detector=` or `sampler=` callables are injected, `CameraPresenceSensor` and `MicrophoneAmbientSensor` return deterministic placeholder values rather than reading physical hardware. Callers must not treat default placeholder outputs as live sensor measurements.
- **No external runtime dependencies:** Core runtime uses only the Python standard library (`dataclasses`, `datetime`, `io`, `math`, `struct`, `wave`, `argparse`, `json`).

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

- **Fail-Closed-Berechtigungen als Standard:** `SensationPermissions` setzt standardmäßig `camera=False` und `microphone=False` (`sound_output=True`). Ein Aufruf von `CameraPresenceSensor.check_presence()` oder `MicrophoneAmbientSensor.sample_ambient()` ohne explizite Freigabe löst `PermissionError` aus.
- **Zero-Egress-RAM-Only-Datenmodell:** `PresenceObservation` trägt `zero_egress_ram_only=True`, und das Paket führt keinerlei Netzwerkaufrufe aus (`boundaries.network: "none"` in `ellmos-module.v2.json`). Das Flag beschreibt die Paketarchitektur; Betriebssystem-Sandbox und Hardware-Zugriffsrechte liegen in der Verantwortung der aufrufenden Umgebung.
- **Platzhalter-Grenze (`v0.1.0`):** Ohne übergebene `detector=`- bzw. `sampler=`-Funktionen liefern `CameraPresenceSensor` und `MicrophoneAmbientSensor` feste Platzhalterwerte und lesen keine physische Hardware aus. Standardausgaben dürfen nicht als echte Live-Messung interpretiert werden.
- **Keine externen Laufzeitabhängigkeiten:** Die Laufzeit nutzt ausschließlich die Python-Standardbibliothek (`dataclasses`, `datetime`, `io`, `math`, `struct`, `wave`, `argparse`, `json`).

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
