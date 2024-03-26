import os
import ifcopenshell
import pandas as pd
import ifcopenshell.util.selector


def _get_depth_range(depth):
    # Skip if depth is not a number
    if not isinstance(depth, float):
        return 'NaN'
    if depth < 1.5:
        return '0 - 1.5'
    elif depth < 2:
        return '1.5 - 2'
    elif depth < 2.5:
        return '2 - 2.5'
    elif depth < 3:
        return '2.5 - 3'
    elif depth < 4:
        return '3 - 4'
    elif depth < 5:
        return '4 - 5'
    elif depth < 8:
        return '5 - 8'
    elif depth < 10:
        return '8 - 10'
    else:
        return '10+'


def _extract(model: ifcopenshell.file) -> tuple:
    qto_water_gas = list()
    for pipe in model.by_type("IfcFlowStorageDevice"):
        psets = ifcopenshell.util.element.get_psets(pipe)
        if "Wasserleitung" not in psets:
            continue
        data = psets["Wasserleitung"]
        qto_water_gas.append({
            "Typ": data["LTYPE"],
            "Nenndurchmesser": data["DIA_NOM"] * 1000,  # in mm
            "Innendurchmesser": data["DIA"] * 1000,  # in mm
            "Außendurchmesser": data["DIA_OUT"] * 1000,  # in mm
            "Material": data["MATERIAL"],
            "Baustatus": data["STATUS"],
            "Länge": data["LENGTH"],
        })

    # Haltungen, Leitungen
    qto_sewers = list()
    for sewer in ifcopenshell.util.selector.filter_elements(model, "IfcFlowSegment, IfcFlowTreatmentDevice"):
        psets = ifcopenshell.util.element.get_psets(sewer)
        if "Haltung" not in psets and "Leitung" not in psets:
            continue
        data = psets["Haltung"] if "Haltung" in psets else psets["Leitung"]
        # check if this is really a sewer. If not, skip it
        # This sometimes happens because BBSoft wildy attaches psets.
        if "HYD_PRINCIP" not in data:
            continue
        qto_sewers.append({
            "Typ": data["HYD_PRINCIP"],
            "Höhe": data["HYD_PROFH"] * 1000,  # in mm
            "Material": data["OTH_MATERIAL"],
            "Baustatus": data["STATUS"],
            "Rohrlänge": data["LENGTH2D"],
            "Name:": data["ID_NAME"],
            "Von-Schacht": data["ID_DRAIN1"],
            "Nach-Schacht": data["ID_DRAIN2"],
        })

    # Straßeneinläufe
    qto_inlets = list()
    for inlet in model.by_type("IfcFlowMovingDevice"):
        psets = ifcopenshell.util.element.get_psets(inlet)
        if "Straßeneinlauf" not in psets:
            continue
        data = psets["Straßeneinlauf"]
        qto_inlets.append({
            "Breite": data["SIZE_A"] * 1000,  # in mm
            "Länge": data["SIZE_B"] * 1000,  # in mm
            "Bezeichnung": f"{data['SIZE_A']*1000 }x{data['SIZE_B']*1000}",
            "Tiefe": data["POS_DZ"],
            "Baustatus": data["STATUS"],
        })

    # Schächte
    qto_manholes = list()
    for manhole in model.by_type("IfcFlowFitting"):
        psets = ifcopenshell.util.element.get_psets(manhole)
        if "Schacht" not in psets:
            continue
        data = psets["Schacht"]
        qto_manholes.append({
            "Typ": data["TYP"],
            "Durchmesser": data["SIZE_A"] * 1000,  # in mm
            "Tiefe": data["POS_DZ"],
            "Baustatus": data["STATUS"],
            "Tiefenbereich": _get_depth_range(data["POS_DZ"])
        })
    return qto_water_gas, qto_sewers, qto_inlets, qto_manholes


def _write_to_excel(qto_water_gas, qto_sewers, qto_inlets, qto_manholes, ifc_file_path) -> None:
    # Write DataFrame to Excel file
    excel_file_path = os.path.splitext(ifc_file_path)[0] + '_Mengen.xlsx'
    with pd.ExcelWriter(excel_file_path) as writer:
        # Check first if entities exist in IFC file to prevent key error
        if (len(qto_water_gas) > 0):
            # Write Wasser- und Gasleitungen DataFrame to Excel
            df_water_gas = pd.DataFrame(qto_water_gas)
            df_water_gas.to_excel(writer, sheet_name='Wasser_Gas', index=False)
            # Create pivot table for Wasser- und Gasleitungen
            df_filtered_water_gas = df_water_gas[df_water_gas['Baustatus'] == '1']
            pivot_table_water_gas = pd.pivot_table(df_filtered_water_gas, values='Länge', index=[
                'Innendurchmesser', 'Material'], aggfunc='sum')
            # Add pivot table for Wasser- und Gasleitungen to new sheet
            pivot_table_water_gas.to_excel(
                writer, sheet_name='Wasser_Gas_Auswertung')

        if (len(qto_sewers) > 0):
            # Write Haltungen, Leitungen DataFrame to Excel
            df_sewers = pd.DataFrame(qto_sewers)
            df_sewers.to_excel(
                writer, sheet_name='Haltungen_Leitungen', index=False)
            # Create pivot table for Haltungen, Leitungen
            df_filtered_sewers = df_sewers[df_sewers['Baustatus'] == '1']
            pivot_table_sewers = pd.pivot_table(df_filtered_sewers, values='Rohrlänge', index=[
                'Typ', 'Material'], aggfunc='sum')
            # Add pivot table for Haltungen, Leitungen to new sheet
            pivot_table_sewers.to_excel(
                writer, sheet_name='Haltungen_Leitungen_Auswertung')

        if (len(qto_inlets) > 0):
            # Write Straßeneinläufe DataFrame to Excel
            df_inlets = pd.DataFrame(qto_inlets)
            df_inlets.to_excel(
                writer, sheet_name='Straßeneinläufe', index=False)
            # Create pivot table for Straßeneinläufe
            pivot_table_inlets = pd.pivot_table(df_inlets, values='Tiefe', index=[
                'Bezeichnung'], aggfunc='count')
            # Add pivot table for Straßeneinläufe to new sheet
            pivot_table_inlets.to_excel(
                writer, sheet_name='Straßeneinläufe_Auswertung')

        if (len(qto_manholes) > 0):
            # Write Schächte DataFrame to Excel
            df_manholes = pd.DataFrame(qto_manholes)

            # Add the new column to the dataframe
            df_manholes.to_excel(
                writer, sheet_name='Schächte', index=False)

            # Create pivot table for Schächte. group and count by depth range
            df_filtered_manholes = df_manholes[df_manholes['Baustatus'] == '1']
            pivot_table_manholes = pd.pivot_table(df_filtered_manholes, values="Tiefe", index=[
                'Typ', 'Durchmesser', 'Tiefenbereich'], aggfunc='count').rename(columns={'Tiefe': 'Anzahl'})
            # Add pivot table for Schächte to new sheet
            pivot_table_manholes.to_excel(
                writer, sheet_name='Schächte_Auswertung')

            # Find manholes with multiple incoming sewers. For this we make use of the "Von-Schacht" column
            # and count the number of occurences of each value. We then filter for those that occur more than once.
            df_multiple_inlets = df_sewers[df_sewers['Von-Schacht'].notnull()]
            df_multiple_inlets = df_multiple_inlets[df_multiple_inlets.duplicated(
                subset='Von-Schacht', keep=False)]
            df_multiple_inlets.to_excel(
                writer, sheet_name='Zusätzliche Anschlüsse', index=False)


def get(ifc_file_path: str) -> None:
    model = ifcopenshell.open(ifc_file_path)
    qto_water_gas, qto_sewers, qto_inlets, qto_manholes = _extract(model)
    _write_to_excel(qto_water_gas, qto_sewers, qto_inlets,
                    qto_manholes, ifc_file_path)
