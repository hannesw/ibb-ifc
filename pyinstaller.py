import PyInstaller.__main__
from pathlib import Path

HERE = Path(__file__).parent.absolute()
path_to_main = str(HERE / "main.py")


def install():
    PyInstaller.__main__.run([
        "ibb_ifc\\gui.py",
        '--onefile',
        '--windowed',
        # other pyinstaller options...
    ])
