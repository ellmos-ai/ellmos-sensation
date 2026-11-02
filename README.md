# ellmos-sensation

Berechtigungsgesteuerte Gerätesensorik (Kamera-Präsenz, Mikrofon-Umgebung, Sounderzeugung) & Open-Compute-Präsenz-Gate für BACH und Open-Ocean (`OCEAN-SENSATION-01`, BACH `#3765` / Ocean `#535`).

## Kernfunktionen

1. **Zero-Egress Kamera-Präsenzprüfung (`CameraPresenceSensor`):**
   - Prüft lokal im RAM (*„Bin ich gerade am PC?"*), ob eine Person vor dem Bildschirm sitzt (`user_present_at_pc: bool`, `person_count: int`, `confidence: float`).
   - **Fail-Closed Berechtigungs-Gate:** Ohne explizite `camera`-Berechtigung (`SensationPermissions.camera=True`) wird kein Kamerazugriff ausgeführt (`PermissionError`).
2. **Open-Compute Präsenz-Gate (`OpenComputePresenceGate`):**
   - `should_pause_open_compute()` verhindert automatisch störende Maus-/Tastatur-Automation (`open-compute`), sobald der Nutzer aktiv vor dem PC erkannt wird oder Eingaben tätigt.
3. **Mikrofon-Ambiente (`MicrophoneAmbientSensor`) & Sounderzeugung (`SoundSynthesizer`):**
   - Ambient-Geräuschpegel (`ambient_db`, `speech_detected`) und dezente akustische Earcons/Hinweistöne (`chime`, `focus_pulse`, `alert_soft`), jeweils strikt an `microphone`- bzw. `sound_output`-Berechtigungen gekoppelt.
