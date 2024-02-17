**Hinweis: Das Programm ist in einer sehr frühen Phase und ist als Pre-Alpha anzusehen.**

# BBSoft IFC-Verarbeitung

Diese Skripte verarbeiten eine von [BBSoft®](https://bbsoft.de/cont/cont_software.php) erzeugte IFC-Datei. Hierbei werden verschiedene Korrekturen vorgenommen:

- Verwendung von gültigen IfcPropertyTypes. Standardmäßig werden alle Datenbankfelder als String ausgegeben. Diese macht eine Weiterverarbeitung z. B. mit einem AVA-Programm sehr schwierig.
- Die Textfragmente "(ed.)" und "(ber.)" werden aus den Kanalhaltungen entfernt.
- An die Schachtnamen wird standardmäßig ein ",-" bzw. falls vorhanden der Straßenname hinzugefügt. Dieses wird entfernt.
- Verschiedene Angaben werden in Meter umgewandelt.

# Massenextraktion

Zusätzlich werden verschiedene Massen extrahiert. Diese Funktionalität ist noch sehr rudimentär.

# Verwendung

Das Projekt nutzt den Python Paketmanager [Poetry](https://python-poetry.org/docs/).

```
poetry install
poetry run python ibb_ifc\main.py "Pfad\Zur\IFC-Datei.ifc"
```

(C) 2024 IBB Wörn Ingenieure GmbH
