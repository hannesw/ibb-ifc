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
    # Look for the properties "ID_DRAIN1" and "ID_DRAIN2" in the Schacht pset. Remove ",-" from the end of the strings.
    for sewer in ifcopenshell.util.selector.filter_elements(model, "IfcFlowSegment, IfcFlowTreatmentDevice"):
        psets = ifcopenshell.util.element.get_psets(sewer)
        for pset in psets:
            print(pset.Name)
        if "Haltung" not in psets and "Leitung" not in psets:
            continue
        if "Haltung" in psets:
            # skip if key error ID_DRAIN1 or ID_DRAIN2. It's likely that this is not a valid sewer with geometry
            if "ID_DRAIN1" not in psets["Haltung"] or "ID_DRAIN2" not in psets["Haltung"]:
                continue
            psets["Haltung"]["ID_DRAIN1"] = psets["Haltung"]["ID_DRAIN1"].replace(
                ",-", "")
            psets["Haltung"]["ID_DRAIN2"] = psets["Haltung"]["ID_DRAIN2"].replace(
                ",-", "")
        else:
            if "ID_DRAIN1" not in psets["Leitung"] or "ID_DRAIN2" not in psets["Leitung"]:
                continue
            psets["Leitung"]["ID_DRAIN1"] = psets["Leitung"]["ID_DRAIN1"].replace(
                ",-", "")
            psets["Leitung"]["ID_DRAIN2"] = psets["Leitung"]["ID_DRAIN2"].replace(
                ",-", "")


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

    print(f"Changed {total} properties {name}")


def process(ifc_file_path) -> str:
    if not ifc_file_path.endswith(".ifc"):
        raise ValueError("Invalid file format. Only IFC files are supported.")

    new_file_path = os.path.splitext(ifc_file_path)[0] + "_processed.ifc"
    model = ifcopenshell.open(ifc_file_path)

    _correct_manhole_names(model)

    for name, dimension_factor in replacing_properties:
        _change_property_type(model, name, dimension_factor)

    print(f"Saving modified file to {new_file_path}")
    model.write(new_file_path)
    print(f"Modified IFC file saved as {new_file_path}")

    return new_file_path
