import ifcopenshell
import ezdxf
from ezdxf import zoom


def _coords(element):
    matrix = ifcopenshell.util.placement.get_local_placement(
        element.ObjectPlacement)
    return matrix[:, 3][:3]


def run(ifc_file_path: str) -> None:
    model = ifcopenshell.open(ifc_file_path)

    sewers = ifcopenshell.util.selector.filter_elements(
        model, "IfcFlowSegment,Haltung.ID_NAME != NULL")

    dxf_file = ezdxf.new(dxfversion='R2010')
    dxf_file.header['$INSUNITS'] = 6  # in meters
    msp = dxf_file.modelspace()

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

        coords = _coords(s)
        msp.add_circle(center=(coords[0], coords[1]),
                       radius=5, dxfattribs={'color': 1})

    zoom.extents(msp)
    dxf_file.saveas(f'{ifc_file_path}.dxf'.replace('.ifc', ''))
