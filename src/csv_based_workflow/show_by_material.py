# Python Script, API Version = V241
# type: ignore
# ruff: noqa: F821
# ruff: noqa: E402
import csv
import os
import re

import clr

clr.AddReference("System.Windows.Forms")
clr.AddReference("System.Drawing")
from System.Drawing import Point
from System.Windows.Forms import (
    AnchorStyles,
    Button,
    CheckedListBox,
    DialogResult,
    Form,
    FormStartPosition,
    Label,
)


class MaterialsForm(Form):
    def __init__(self, materials):
        self.Text = "Material selection"
        self.Width = 300
        self.Height = 400
        self.StartPosition = FormStartPosition.CenterScreen

        self.label = Label()
        self.label.Text = "Select materials:"
        self.label.Location = Point(20, 20)
        self.Controls.Add(self.label)

        self.checkedListBox = CheckedListBox()
        self.checkedListBox.CheckOnClick = True
        self.checkedListBox.Location = Point(20, 50)
        self.checkedListBox.Width = 240
        self.checkedListBox.Height = 250
        self.checkedListBox.ScrollAlwaysVisible = True
        for material in materials:
            self.checkedListBox.Items.Add(material)
        self.Controls.Add(self.checkedListBox)

        self.button = Button()
        self.button.Text = "Finish"
        self.button.Location = Point(20, 320)
        self.button.Anchor = AnchorStyles.Bottom | AnchorStyles.Left
        self.button.Click += self.on_finish
        self.Controls.Add(self.button)

        self.selected_materials = []

    def on_finish(self, _sender, _event):
        self.selected_materials = [
            self.checkedListBox.Items[i]
            for i in range(self.checkedListBox.Items.Count)
            if self.checkedListBox.GetItemChecked(i)
        ]
        self.DialogResult = DialogResult.OK
        self.Close()


def get_selected_materials(materials):
    form = MaterialsForm(sorted(materials))
    result = form.ShowDialog()
    if result == DialogResult.OK:
        selected_materials = []
        for material in form.selected_materials:
            if material == "No material specified":
                selected_materials.append("")
            else:
                selected_materials.append(material)
        return form.selected_materials
    MessageBox.Show("No materials selected!")
    raise ValueError


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


def get_material_names_from_dict(comps_dict):
    material_names = set()
    for comp in comps_dict.values():
        material_name = comp["MATERIAL"]
        if material_name != "":
            material_names.add(comp["MATERIAL"])
        else:
            material_names.add("No material specified")
    return material_names


def get_components_to_show(sc_comps, csv_comps, materials_to_show):
    components_to_show = []
    for comp in sc_comps.values():
        comp_material = csv_comps[comp.GetName()]["MATERIAL"]
        if comp_material in materials_to_show:
            components_to_show.append(comp)
    return components_to_show


def hide_all_components():
    sel = Selection.Create(GetRootPart().GetAllBodies())
    visibility = VisibilityType.Hide
    inSelectedView = False
    ViewHelper.SetObjectVisibility(sel, visibility, inSelectedView)


def show_components(comps):
    bodies = []
    for comp in comps:
        bodies += comp.GetBodies()
    sel = Selection.Create(bodies)
    visibility = VisibilityType.Show
    inSelectedView = False
    ViewHelper.SetObjectVisibility(sel, visibility, inSelectedView)


def main():
    csv_comps = get_dict_from_csv()
    sc_comps = get_dict_of_components_with_bodies()

    material_names = get_material_names_from_dict(csv_comps)
    materials_to_show = get_selected_materials(material_names)
    components_to_show = get_components_to_show(sc_comps, csv_comps, materials_to_show)

    hide_all_components()
    show_components(components_to_show)
    ViewHelper.ZoomToEntity()


main()
