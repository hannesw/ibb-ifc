import importlib
import os
import click


def _get_module_path(module_name: str) -> str:
    """Extracts the path of the specified module at runtime.

    Args:
        module_name: The name of the module to import.

    Returns:
        The path to the directory containing the imported module, or None if not found.
    """
    try:
        module = importlib.import_module(module_name)
        return os.path.dirname(module.__file__)
    except ModuleNotFoundError:
        return None


@click.command()
@click.option(
    "--target", default="gui", type=click.Choice(["gui", "cli"], case_sensitive=False)
)
def run(target: str):
    output = ""

    packages = ["ifcopenshell"]
    if target == "gui":
        packages.append("customtkinter")
    for package in packages:
        package_path = _get_module_path(package)
        output += f'--add-data "{package_path};{package}" '

    print(output)


if __name__ == "__main__":
    run()
