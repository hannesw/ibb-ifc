import subprocess
import ifcopenshell
import ezdxf
from ezdxf import zoom
import os
from glob import glob


def _draw_check_marker(msp, coords, text=None, color=1, layer="0"):
    msp.add_circle(
        center=(coords[0], coords[1]),
        radius=3,
        dxfattribs={"color": color, "layer": layer},
    )
    if text:
        msp.add_mtext(
            text,
            dxfattribs={
                "color": color,
                "char_height": 0.6,
                "attachment_point": 5,  # align text mid-center
                "layer": layer,
            },
        ).set_location((coords[0], coords[1]))


def _sewer_midpoint(pset):
    try:
        x1 = pset["ABS_1X"]
        y1 = pset["ABS_1Y"]
        x2 = pset["ABS_2X"]
        y2 = pset["ABS_2Y"]
    except KeyError:
        return None
    return (x1 + x2) / 2, (y1 + y2) / 2


def _sewer_check_slope(pset):
    try:
        slope = pset["HYD_GRAD_PP"]
    except KeyError:
        return None
    if slope < 0.01:
        return slope
    return None


def _setup_dxf() -> ezdxf.layouts.Modelspace:
    dxf_file = ezdxf.new(dxfversion="R2010")
    dxf_file.header["$INSUNITS"] = 6  # in meters
    msp = dxf_file.modelspace()

    dxf_file.layers.new(name="Kanal", dxfattribs={"color": 1})
    dxf_file.layers.new(name="Wasserleitung", dxfattribs={"color": 5})

    return dxf_file, msp


def _convert_to_DWG(dxf_path: str) -> bool:
    """
    If the ODA File Converter is installed on the system, this function will
    convert the file to a DWG file, wich directly can be attachted as XREF.
    """
    if os.name != "nt":  # Check for Windows OS
        return False

    oda_path = None

    programs_path = os.environ.get("ProgramFiles")
    for programs_dir in os.listdir(programs_path):
        # Skip files
        if not os.path.isdir(os.path.join(programs_path, programs_dir)):
            continue

        # Check for ODA File Converter
        if "ODA" in programs_dir:
            oda_path = os.path.join(programs_path, programs_dir)
            break

    if not oda_path:
        print("ODA File Converter not found")
        return False

    # Check for all available versions
    converter_folders = glob(os.path.join(oda_path, "ODAFileConverter *"))
    if not converter_folders:
        print("ODA File Converter not found")
        return False
    # Check for the latest version
    latest_version = max(converter_folders, key=os.path.dirname)

    converter_exe = os.path.join(latest_version, "ODAFileConverter.exe")
    input_path = os.path.abspath(os.path.dirname(dxf_path))
    print(input_path)
    cmd = [
        converter_exe,
        input_path,  # Quoted input folder
        input_path,  # Quoted output folder
        "ACAD2013",  # Output version
        "DWG",  # Output File type
        "0",  # Recurse Input Folder
        "0",  # Audit each file
        "*.DXF",  # Input files filter
    ]
    subprocess.run(cmd)

    return True


def run(ifc_file_path: str) -> None:
    model = ifcopenshell.open(ifc_file_path)
    dxf_file, msp = _setup_dxf()

    sewers = ifcopenshell.util.selector.filter_elements(
        model, "IfcFlowSegment,Haltung.ID_NAME != NULL"
    )
    laterals = ifcopenshell.util.selector.filter_elements(
        model, "IfcFlowTreatmentDevice,Leitung.ID_NAME != NULL"
    )

    for s in sewers:
        pset = ifcopenshell.util.element.get_pset(s, "Haltung")
        if _sewer_check_slope(pset):
            _draw_check_marker(
                msp,
                _sewer_midpoint(pset),
                f"Gefälle: {round(pset['HYD_GRAD_PP'] * 1000, 1)} ‰",
                color=256,
                layer="Kanal",
            )

    for lateral in laterals:
        pset = ifcopenshell.util.element.get_pset(lateral, "Leitung")
        if _sewer_check_slope(pset):
            _draw_check_marker(
                msp,
                _sewer_midpoint(pset),
                f"Gefälle: {round(pset['HYD_GRAD_PP'] * 1000, 1)} ‰",
                color=256,
                layer="Kanal",
            )

    zoom.extents(msp)
    dxf_path = f"{ifc_file_path}.dxf".replace(".ifc", "")
    dxf_file.saveas(dxf_path)

    dwg_available = _convert_to_DWG(dxf_path)
    if dwg_available:
        os.remove(dxf_path)
