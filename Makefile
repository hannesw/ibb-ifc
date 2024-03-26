all: cli gui gui-dev

cli:
	pyinstaller --onefile --noconfirm $(CLI_HELPER_OUTPUT) cli.py -n cli

gui:
	pyinstaller --onedir --noconfirm --windowed $(GUI_HELPER_OUTPUT) gui.py -n gui

gui-dev:
	pyinstaller --onedir --noconfirm $(GUI_HELPER_OUTPUT) gui.py -n gui-dev

GUI_HELPER_OUTPUT := $(shell python make_helper.py --target=gui)

CLI_HELPER_OUTPUT := $(shell python make_helper.py --target=cli)
