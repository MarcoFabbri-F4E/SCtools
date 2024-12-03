# Python Script, API Version = V241
# type: ignore
# ruff: noqa: F821, UP032
import csv
import os
import re


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


def get_selected_components(csv_dict):
    components = set()
    for selected in Selection.GetActive().Items:
        if selected.Parent.GetName() not in csv_dict:
            MessageBox.Show(selected.Parent.GetName() + " is missing from CSV!")
            raise KeyError
        components.add(selected.Parent)
    return components


def get_component_info(component, csv_dict):
    comp_name = component.GetName()
    try:
        original_volume = float(csv_dict[comp_name]["ORIGINAL VOLUME [cm3]"])
    except ValueError as exc:
        MessageBox.Show("Invalid volume in CSV for {}!".format(comp_name))
        raise exc

    material = csv_dict[comp_name]["MATERIAL"]
    if not material:
        MessageBox.Show("Material not defined for {}!".format(comp_name))
        raise KeyError

    try:
        density = float(csv_dict[comp_name]["DENSITY [g/cm3]"])
    except ValueError as exc:
        MessageBox.Show("Invalid density in CSV for {}!".format(comp_name))
        raise exc

    component_id = re.search("\d+", csv_dict[comp_name]["Component ID"]).group()

    return original_volume, material, density, component_id


def prepare_component_row(csv_dict, material_mix_by_mass, total_volume, component_ids):
    csv_columns = csv_dict.values()[0].keys()
    component_row = {key: "" for key in csv_columns}
    for key in component_row.keys():
        if "Level" in key:
            component_row[key] = "-"

    max_id = max(int(key.replace("Component", "")) for key in csv_dict.keys())
    new_id = max_id + 1
    component_row["Component ID"] = "Component{}".format(new_id)
    component_row["ORIGINAL VOLUME [cm3]"] = total_volume
    component_row["MATERIAL"] = "Mix{}".format(new_id)
    component_row["DENSITY [g/cm3]"] = sum(material_mix_by_mass.values()) / total_volume

    comment = "Homogenized from components: {}".format(", ".join(component_ids)) + ". "
    comment += "Material mix by mass [g]: "
    for material, mass in material_mix_by_mass.items():
        comment += "{}: {:.2f}, ".format(material, mass)
    comment = comment[:-2] + "."
    component_row["COMMENT"] = comment
    return component_row


def write_new_component_to_csv(component_row):
    csv_file_path = GetRootPart().Document.Path[:-6] + ".csv"
    with open(csv_file_path) as infile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames
    with open(csv_file_path, mode="ab") as infile:
        writer = csv.DictWriter(infile, fieldnames=fieldnames)
        writer.writerow(component_row)


def create_new_component(new_component_id):
    pass


def main():
    csv_dict = get_dict_from_csv()
    components = get_selected_components(csv_dict)

    total_volume = 0
    material_mix_by_mass = {}  # material_name: mass
    component_ids = []
    for component in components:
        original_volume, material, density, component_id = get_component_info(
            component, csv_dict
        )
        total_volume += original_volume
        material_mix_by_mass[material] = (
            material_mix_by_mass.get(material, 0.0) + original_volume * density
        )
        component_ids.append(component_id)

    component_row = prepare_component_row(
        csv_dict, material_mix_by_mass, total_volume, component_ids
    )
    write_new_component_to_csv(component_row)
    create_new_component(component_row["Component ID"])


main()
