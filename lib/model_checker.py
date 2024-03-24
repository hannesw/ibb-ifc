import ifcopenshell
import ezdxf
from ezdxf import zoom


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


def run(ifc_file_path: str) -> None:
    model = ifcopenshell.open(ifc_file_path)

    dxf_file = ezdxf.new(dxfversion="R2010")
    dxf_file.header["$INSUNITS"] = 6  # in meters
    msp = dxf_file.modelspace()

    sewers = ifcopenshell.util.selector.filter_elements(
        model, "IfcFlowSegment,Haltung.ID_NAME != NULL"
    )
    for s in sewers:
        pset = ifcopenshell.util.element.get_pset(s, "Haltung")
        if _sewer_check_slope(pset):
            _draw_check_marker(
                msp,
                _sewer_midpoint(pset),
                f"Gefälle: {round(pset['HYD_GRAD_PP'] * 1000, 1)} ‰",
            )

        laterals = ifcopenshell.util.selector.filter_elements(
            model, "IfcFlowTreatmentDevice,Leitung.ID_NAME != NULL"
        )
        for lateral in laterals:
            pset = ifcopenshell.util.element.get_pset(lateral, "Leitung")
            if _sewer_check_slope(pset):
                _draw_check_marker(
                    msp,
                    _sewer_midpoint(pset),
                    f"Gefälle: {round(pset['HYD_GRAD_PP'] * 1000, 1)} ‰",
                )

    zoom.extents(msp)
    dxf_file.saveas(f"{ifc_file_path}.dxf".replace(".ifc", ""))
