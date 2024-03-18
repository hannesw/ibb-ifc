import ifcopenshell
import ezdxf
from ezdxf import zoom

"""
Extracts the placement matrix from an IFC element and returns the coordinates.
"""


def _coords(element):
    matrix = ifcopenshell.util.placement.get_local_placement(
        element.ObjectPlacement)
    return matrix[:, 3][:3]


"""
Calculates the midpoint of an sewer or lateral and returns the coordinates.
"""


def _sewer_midpoint(pset):
    try:
        x1 = pset["ABS_1X"]
        y1 = pset["ABS_1Y"]
        x2 = pset["ABS_2X"]
        y2 = pset["ABS_2Y"]
    except KeyError:
        return None
    return (x1 + x2) / 2, (y1 + y2) / 2


def run(ifc_file_path: str) -> None:
    model = ifcopenshell.open(ifc_file_path)

    dxf_file = ezdxf.new(dxfversion='R2010')
    dxf_file.header['$INSUNITS'] = 6  # in meters
    msp = dxf_file.modelspace()

    sewers = ifcopenshell.util.selector.filter_elements(
        model, "IfcFlowSegment,Haltung.ID_NAME != NULL")
    for s in sewers:
        pset = ifcopenshell.util.element.get_pset(s, "Haltung")
        # Skip if keyerror
        try:
            slope = pset["HYD_GRAD_PP"]
        except KeyError:
            continue
        if slope < 0.01:
            print(
                f"Slope of {pset['ID_NAME']} is too low: {round(slope * 1000, 1)} ‰")
            # coords = _coords(s) # This is a more general approach but makes it difficult to identify the sewer
            coords = _sewer_midpoint(pset)
            msp.add_circle(center=(coords[0], coords[1]),
                           radius=3, dxfattribs={'color': 1})
            msp.add_mtext(f"Gefälle: {round(slope * 1000, 1)} ‰",
                          dxfattribs={'color': 1, 'char_height': 0.6, 'attachment_point': 5}).set_location((coords[0], coords[1]))

        laterals = ifcopenshell.util.selector.filter_elements(
            model, "IfcFlowSegment,Leitung.ID_NAME != NULL")
        for l in laterals:
            pset = ifcopenshell.util.element.get_pset(l, "Leitung")
            # Skip if keyerror
            try:
                slope = pset["HYD_GRAD_PP"]
            except KeyError:
                continue
            if slope < 0.01:
                print(
                    f"Slope of {pset['ID_NAME']} is too low: {round(slope * 1000, 1)} ‰")
                # coords = _coords(l) # This is a more general approach but makes it difficult to identify the lateral
                coords = _sewer_midpoint(pset)
                msp.add_circle(center=(coords[0], coords[1]),
                               radius=3, dxfattribs={'color': 1})
                msp.add_mtext(f"Gefälle: {round(slope * 1000, 1)} ‰",
                              dxfattribs={'color': 5, 'char_height': 0.6, 'attachment_point': 5}).set_location((coords[0], coords[1]))

    zoom.extents(msp)
    dxf_file.saveas(f'{ifc_file_path}.dxf'.replace('.ifc', ''))
