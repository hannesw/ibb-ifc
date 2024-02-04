import ifcopenshell
import os
import ifcopenshell.util.selector

dimension_factors = {
    "m": {
        "factor": 1,
        "unit": "m"
    },
    "cm": {
        "factor": 0.01,
        "unit": "cm"
    },
    "mm": {
        "factor": 0.001,
        "unit": "mm"
    },
    "%": {
        "factor": 0.01,
        "unit": "%"
    },
}

replacing_properties = [
    # Haltungen
    ["ABS_1X", dimension_factors["m"]],  # Rechtswert oben
    ["ABS_1Y", dimension_factors["m"]],  # Hochwert oben
    ["ABS_1Z", dimension_factors["m"]],  # Höhe oben
    ["ABS_2X", dimension_factors["m"]],  # Rechtswert unten
    ["ABS_2Y", dimension_factors["m"]],  # Hochwert unten
    ["ABS_2Z", dimension_factors["m"]],  # Höhe unten
    ["HYD_GRAD_PP", dimension_factors["%"]],  # Rohrgefälle
    ["HYD_LEN", dimension_factors["m"]],  # Haltungslänge
    ["HYD_OCCUP", dimension_factors["%"]],  # Hydraulische Auslastung
    ["HYD_PROFH", dimension_factors["mm"]],  # Profilhöhe
    ["HYD_PROFW", dimension_factors["mm"]],  # Profilbreite
    ["LENGTH2D", dimension_factors["m"]],  # Rohrlänge (2D)
    ["LENGTH3D", dimension_factors["m"]],  # Rohrlänge (3D)
    ["OWN_1Z", dimension_factors["m"]],  # Tiefe oben
    ["OWN_2Z", dimension_factors["m"]],  # Tiefe unten

    # Schächte
    ["POS_DZ", dimension_factors["m"]],  # Schachttiefe
    ["POS_X", dimension_factors["m"]],  # Rechtswert
    ["POS_Y", dimension_factors["m"]],  # Hochwert
    ["POS_ZLOW", dimension_factors["m"]],  # Sohlhöhe
    ["SIZE_A", dimension_factors["m"]],  # Schachtdurchmesser/-breite
    ["SIZE_B", dimension_factors["m"]],  # Länge
    ["WALL_TCHICKNESS", dimension_factors["mm"]],  # Wandstärke

    # Wasserleitungen
    ["DIA", dimension_factors["mm"]],  # Rohrdurchmesser innen
    ["DIA_NOM", dimension_factors["mm"]],  # Rohrdurchmesser Nenngröße
    ["DIA_OUT", dimension_factors["mm"]],  # Rohrdurchmesser außen
    ["LAYINGDEPTH", dimension_factors["m"]],  # Verlegetiefe
    ["LENGTH", dimension_factors["m"]],  # Rohrlänge
]


def _to_float(value):
    value = value.replace(" ", "").replace("(ber.)", "").replace("(ed.)", "")
    if value == "":
        return None
    return float(value)


def _correct_manhole_names(model):
    sewers = ifcopenshell.util.selector.filter_elements(
        model, "IfcFlowSegment,Haltung.ID_NAME != NULL")
    for s in sewers:
        pset = ifcopenshell.util.element.get_pset(s, "Haltung")
        # Skip if keyerror
        try:
            pset["ID_DRAIN1"] = pset["ID_DRAIN1"].replace(",-", "")
            pset["ID_DRAIN2"] = pset["ID_DRAIN2"].replace(",-", "")
        except KeyError:
            continue

    branches = ifcopenshell.util.selector.filter_elements(
        model, "IfcFlowTreatmentDevice")
    for b in branches:
        pset = ifcopenshell.util.element.get_pset(b, "Leitung")
        # Skip if keyerror
        try:
            pset["ID_DRAIN1"] = pset["ID_DRAIN1"].replace(",-", "")
            pset["ID_DRAIN2"] = pset["ID_DRAIN2"].replace(",-", "")
        except KeyError:
            continue


def _change_property_type(model, name, dimension_factor):
    properties = ifcopenshell.util.selector.filter_elements(
        model,
        f"IfcPropertySingleValue, Name={name}"
    )

    total = len(properties)
    for i, prop in enumerate(properties):
        value = _to_float(prop.NominalValue.wrappedValue)
        if value is None:
            continue

        value *= dimension_factor["factor"]
        if dimension_factor["unit"] == "%":
            ratio_measure = model.create_entity(
                "IfcRatioMeasure", value)
            prop.NominalValue = ratio_measure
        else:
            length_measure = model.create_entity(
                "IfcPositiveLengthMeasure", value)
            prop.NominalValue = length_measure

    print(f"\tChanged {total} properties {name}")


def process(ifc_file_path) -> str:
    print(f"Opening {ifc_file_path}")
    new_file_path = os.path.splitext(ifc_file_path)[0] + "_processed.ifc"
    print(f"New file path will be {new_file_path}")
    model = ifcopenshell.open(ifc_file_path)

    print(f"Correcting manhole names")
    _correct_manhole_names(model)

    print(f"Changing property types:")
    for name, dimension_factor in replacing_properties:
        _change_property_type(model, name, dimension_factor)

    print(f"Saving modified file")
    model.write(new_file_path)
    print(f"Modified IFC file saved as {new_file_path}")

    return new_file_path
