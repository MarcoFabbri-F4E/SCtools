# Python Script, API Version = V241
# type: ignore
# ruff: noqa: F821
import csv
import os

MAX_DIFF = 1  # maximum volume difference allowed in %
STEP = 1  # in mm


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


def get_total_volume(sc_comp):
    vol = 0.0
    for body in sc_comp.GetBodies():
        vol = vol + body.MassProperties.Mass * 1000000  # cm3
    return vol


def set_components_as_blue_transparent(comps):
    sel = Selection.Create(comps)
    options = SetColorOptions()
    options.FaceColorTarget = FaceColorTarget.Body
    ColorHelper.SetColor(sel, options, ColorHelper.Blue)
    ColorHelper.SetFillStyle(sel, FillStyle.Transparent)


def extrude_faces(sel, component, original_volume):
    step = STEP
    options = ExtrudeFaceOptions()
    options.ExtrudeType = ExtrudeType.ForceIndependent

    current_volume = get_total_volume(component)
    dif = (original_volume - current_volume) / original_volume * 100
    positive_sense = True if dif > 0 else False
    while abs(dif) > MAX_DIFF:
        if dif > 0:
            if not positive_sense:
                step = step * 0.5
                positive_sense = True
            ExtrudeFaces.Execute(sel, MM(step), options)
        else:
            if positive_sense:
                step = step * 0.5
                positive_sense = False
            ExtrudeFaces.Execute(sel, MM(-step), options)
        current_volume = get_total_volume(component)
        dif = (original_volume - current_volume) / original_volume * 100


def main():
    csv_dict = get_dict_from_csv()

    sel = Selection.GetActive()
    body = sel.Items[0].Parent
    component = body.Parent

    try:
        original_volume = float(csv_dict[component.GetName()]["ORIGINAL VOLUME [cm3]"])
    except KeyError:
        MessageBox.Show(component.GetName() + " is missing from CSV!")
        return

    extrude_faces(sel, component, original_volume)
    set_components_as_blue_transparent(component)


main()
