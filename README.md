**Hinweis: Das Programm ist in einer sehr frühen Phase und ist als Alpha-Software anzusehen.**

# Programmbeschreibung

Dieses Programm verarbeitete eine von [BBSoft®](https://bbsoft.de/cont/cont_software.php) erzeugte IFC-Datei, sodass diese mit anderer Software (z.B. für AVA) weiterverarbeitet werden kann.
Zusätzlich können verschiedene Modellprüfungen für die Qualitätskontrolle durchgeführt werden.
Ebenfalls kann eine einfache Massenermittlung in Form einer Excel-Datei erzeugt werden.

## BBSoft IFC-Verarbeitung

Folgende werden verschiedene Korrekturen vorgenommen:

- Verwendung von gültigen IfcPropertyTypes. Standardmäßig werden alle Datenbankfelder als String ausgegeben. Diese macht eine Weiterverarbeitung z. B. mit einem AVA-Programm sehr schwierig.
- Die Textfragmente "(ed.)" und "(ber.)" werden aus den Kanalhaltungen entfernt.
- An die Schachtnamen wird standardmäßig ein ",-" bzw. falls vorhanden der Straßenname hinzugefügt. Dieses wird entfernt.
- Verschiedene Angaben werden in die korrekte Einheit (z. B. Meter) umgewandelt.

## Modellprüfung

Die gefundenen Problemstellen werden in eine DWG-Datei eingefügt, so dass diese hinter die Planung gelegt werden kann.

### Kanal

- [ ] Vollständigkeit: Material
- [ ] Vollständigkeit: Dimension
- [ ] Vollständigkeit: Bauzustand
- [ ] Vollständigkeit: Wandstärke
- [ ] Vollständigkeit: Koordinaten, Höhe
- [ ] Plausibilität: Material
- [ ] Plausibilität: Dimension (z.B. in Abhängigkeit von Material andere Dimensionen)
- [ ] Plausibilität: Wandstärke. Bewegt sich die Wandstärke für das angegebene Material + Dimension in den üblichen Grenzen
- [ ] Plausibilität: Befinden sich die Koordinaten innerhalb von GK oder UTM?
- [ ] Plausibilität: Ist die Höhe in einem üblichen Rahmen.
- [ ] Plausibilität: Gibt es Ausreiser bei der Höhe
- [ ] Plausibilität: Haltungsbezeichnung wie oberer Schacht
- [ ] Fließrichtung entsprechend Gefälle
- [ ] Technik: Hydraulische Auslastung
- [x] Technik: Gefälle ausreichend
- [ ] Technik: Schacht mit ausreichender Tiefe
- [ ] Technik: Absturzhöhe
- [ ] Einlaufhöhe kleiner als Auslaufhöhe

### Wasserleitung

- [ ] Vollständigkeit: Material
- [ ] Vollständigkeit: Dimension
- [ ] Vollständigkeit: Bauzustand
- [ ] Vollständigkeit: Koordinaten, Höhe
- [ ] Plausibilität: Material
- [ ] Plausibilität: Befinden sich die Koordinaten innerhalb von GK oder UTM?
- [ ] Plausibilität: Ist die Höhe in einem üblichen Rahmen.
- [ ] Plausibilität: Gibt es Ausreiser bei der Höhe

# Verwendung

Aktuelle Binaries für Windows können [hier bei Github](https://github.com/ibb-woern/ibb-ifc/releases) heruntergeladen werden.

Für die graphische Benutzoberfläche starten der `gui.exe`.

Für das Kommandozeilenwerkzeug starten der `cli.exe`. Die verfügbaren Optionen können mit `cli.exe --help` angezeigt werden.

Falls der [ODA File Converter](https://www.opendesign.com/guestfiles/oda_file_converter) installiert ist, wird die Modellprüfung als DWG-Datei ausgegeben. Andernfalls als DXF-Datei.

# Entwicklung

## Voraussetzungen

- python mit pip
- Empfehlung für die Verwaltung verschiedener Python-Versionen: [pyenv](https://github.com/pyenv/pyenv) oder [pyenv-win](https://github.com/pyenv-win/pyenv-win)
- [make](https://cmake.org/)

## Starten

```bash
# Installieren der Abhängigkeiten
pip install -r requirements.txt
# Starten des CLI
python cli.py
# Starten des GUI
python gui.py
# Bauen der binaries (.exe)
make

```

# Lizenz

(C) 2024 IBB Wörn Ingenieure GmbH
