# BBSoft IFC-Verarbeitung

Diese Skripte verarbeiten eine von BBSoft erzeugte IFC-Datei. Hierbei werden verschiedene Korrekturen vorgenommen:

- Verwendung von gültigen IfcPropertyTypes. Standardmäßig werden alle Datenbankfelder als String ausgegeben. Diese macht eine Weiterverarbeitung z. B. mit einem AVA-Programm sehr schwierig.
- Die Textfragmente "(ed.)" und "(ber.)" werden aus den Kanalhaltungen entfernt.
- An die Schachtnamen wird standardmäßig ein ",-" hinzugefügt. Dieses wird entfernt.
- Verschiedene Angaben werden in Meter umgewandelt.

# Massenextraktion

Zusätzlich werden verschiedene Massen extrahiert. Diese Funktionalität ist noch sehr rudimentär.

(C) 2024 IBB Wörn Ingenieure GmbH
