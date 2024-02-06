import subprocess


def build_app():
    cmd = [
        "poetry", "run", "pyinstaller", "--onefile",
        "--name=IBB-IFC",
        "--icon=assets/logo-ibb.png",
        "--hidden-import",
        "tkinter",
        "ibb_ifc\\gui.py",
    ]

    # Execute the command
    subprocess.run(cmd)


if __name__ == "__main__":
    build_app()
