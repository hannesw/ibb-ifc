**Hinweis: Das Programm ist in einer sehr frühen Phase und ist als Alpha-Software anzusehen.**

# BBSoft IFC-Verarbeitung

Dieses Programm verarbeitete eine von [BBSoft®](https://bbsoft.de/cont/cont_software.php) erzeugte IFC-Datei. Hierbei werden verschiedene Korrekturen vorgenommen:

- Verwendung von gültigen IfcPropertyTypes. Standardmäßig werden alle Datenbankfelder als String ausgegeben. Diese macht eine Weiterverarbeitung z. B. mit einem AVA-Programm sehr schwierig.
- Die Textfragmente "(ed.)" und "(ber.)" werden aus den Kanalhaltungen entfernt.
- An die Schachtnamen wird standardmäßig ein ",-" bzw. falls vorhanden der Straßenname hinzugefügt. Dieses wird entfernt.
- Verschiedene Angaben werden in die korrekte Einheit (z. B. Meter) umgewandelt.

# Verwendung

Für die graphische Benutzoberfläche starten der `gui.exe`.

Für das Kommandozeilenwerkzeug starten der `cli.exe`. Die verfügbaren Optionen können mit `cli.exe --help` angezeigt werden.

# Entwicklung

## Voraussetzungen

- python mit pip
- Empfehlung für die Verwaltung verschiedener Python-Versionen: [pyenv](https://github.com/pyenv/pyenv) oder [pyenv-win](https://github.com/pyenv-win/pyenv-win)
- [make](https://www.gnu.org/software/make/) oder [make for windows](https://gnuwin32.sourceforge.net/packages/make.htm)

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
