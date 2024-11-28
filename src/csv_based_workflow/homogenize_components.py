# Python Script, API Version = V241
# type: ignore
# ruff: noqa: F821, UP032
import csv
import os


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
    for selected in Selection.GeActive():
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

    return original_volume, material, density


def prepare_component_row(csv_dict, material_mix_by_mass, total_volume):
    csv_columns = csv_dict.values()[0].keys()
    component_row = {key: "" for key in csv_columns}

    max_id = max(int(key.replace("Component", "")) for key in csv_dict.keys())
    new_id = max_id + 1
    component_row["Component ID"] = "Component{}".format(new_id)
    component_row["ORIGINAL VOLUME [cm3]"] = total_volume
    component_row["MATERIAL"] = "Mix{}".format(new_id)
    component_row["DENSITY [g/cm3]"] = sum(material_mix_by_mass.values()) / total_volume
    return component_row


def write_new_component_to_csv(component_row):
    csv_file_path = GetRootPart().Document.Path[:-6] + ".csv"
    with open(csv_file_path, mode="a", newline="") as infile:
        writer = csv.DictWriter(infile, fieldnames=component_row.keys())
        writer.writerow(component_row)


def create_new_component(new_component_id): ...


def main():
    csv_dict = get_dict_from_csv()
    components = get_selected_components(csv_dict)

    total_volume = 0
    material_mix_by_mass = {}  # material_name: mass
    for component in components:
        original_volume, material, density = get_component_info(component, csv_dict)
        total_volume += original_volume
        material_mix_by_mass[material] = (
            material_mix_by_mass.get(material, 0.0) + original_volume * density
        )

    component_row = prepare_component_row(csv_dict, material_mix_by_mass, total_volume)
    write_new_component_to_csv(component_row)
    create_new_component(component_row["Component ID"])


main()
