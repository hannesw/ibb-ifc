all: cli gui gui-dev

cli:
	pyinstaller --onefile --noconfirm main.py -n cli

gui:
	pyinstaller --windowed --noconfirm --onedir gui.py -n gui

gui-dev:
	pyinstaller --onedir --noconfirm gui.py -n gui-dev