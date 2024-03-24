all: cli gui gui-dev

cli:
	pyinstaller --onefile main.py -n cli

gui:
	pyinstaller --windowed --onedir gui.py -n gui

gui-dev:
	pyinstaller --onedir gui.py -n gui-dev