import os
import subprocess

logo_path = os.path.join(os.path.dirname(__file__), "assets", "logo-ibb.png")
assets_path = os.path.join(os.path.dirname(__file__), "assets")
entry_path = os.path.join(os.path.dirname(__file__), "ibb_ifc", "gui.py")


def build_app():
    cmd = [
        "poetry", "run", "pyinstaller", "--onefile",
        "--name=IBB-IFC",
        f"--icon={logo_path}",
        "--windowed",
        # f"--add-data={assets_path}:assets",
        entry_path
    ]

    # Execute the command
    subprocess.run(cmd)


if __name__ == "__main__":
    build_app()
