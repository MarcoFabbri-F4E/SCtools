# Python Script, API Version = V241
# type: ignore
# ruff: noqa: F821
import csv
import os
import re

MAX_DIFF = 1  # maximum volume difference allowed in %


def get_dict_from_csv():
    csv_file_path = GetRootPart().Document.Path[:-6] + ".csv"
    if not os.path.exists(csv_file_path):
        MessageBox.Show("CSV file not found!")
        raise FileNotFoundError
    result_dict = {}
    with open(csv_file_path) as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            result_dict[row["Component ID"]] = row
    return result_dict


def get_dict_of_components_with_bodies():
    dict_components = {}
    components = GetRootPart().GetAllComponents()
    for comp in components:
        bodies = comp.GetBodies()
        if len(bodies) > 0:
            name = comp.GetName()
            if not re.match(r"Component\d+", name):
                MessageBox.Show(name + " does not follow ComponentXXX convention!")
            if name in dict_components:
                MessageBox.Show(name + " is repeated!")
            dict_components[name] = comp
    return dict_components


def get_total_volume(sc_comp):
    vol = 0.0
    for body in sc_comp.GetBodies():
        vol = vol + body.MassProperties.Mass * 1000000  # cm3
    return vol


def get_components_that_exceed_volume_dif(sc_comps, csv_comps):
    volume_exceeded_comps = []

    for name, sc_comp in sc_comps.items():
        if name not in csv_comps:
            MessageBox.Show(name + " is missing from CSV!")
            continue

        original_volume = float(csv_comps[name]["ORIGINAL VOLUME [cm3]"])
        current_volume = get_total_volume(sc_comp)
        dif = (original_volume - current_volume) / original_volume * 100
        if abs(dif) > MAX_DIFF:
            volume_exceeded_comps.append(sc_comp)

    return volume_exceeded_comps


def set_components_as_blue_transparent(comps):
    sel = Selection.Create(comps)
    options = SetColorOptions()
    options.FaceColorTarget = FaceColorTarget.Body
    ColorHelper.SetColor(sel, options, ColorHelper.Blue)
    ColorHelper.SetFillStyle(sel, FillStyle.Transparent)


def set_components_as_red_opaque(comps):
    sel = Selection.Create(comps)
    options = SetColorOptions()
    options.FaceColorTarget = FaceColorTarget.Body
    ColorHelper.SetColor(sel, options, Color.Red)
    ColorHelper.SetFillStyle(sel, FillStyle.Opaque)


def main():
    csv_comps = get_dict_from_csv()
    sc_comps = get_dict_of_components_with_bodies()

    volume_exceeded_comps = get_components_that_exceed_volume_dif(sc_comps, csv_comps)

    if len(volume_exceeded_comps) == 0:
        MessageBox.Show("No components exceeded the maximum volume difference")
        return

    set_components_as_blue_transparent(sc_comps.values())
    set_components_as_red_opaque(volume_exceeded_comps)


main()
