# Python Script, API Version = V241
# type: ignore
# ruff: noqa: F821
import re


def get_dict_of_bodies():
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
            dict_components[name] = comp.GetBodies()
    return dict_components


def get_sorted_keys_by_number(d):
    return sorted(d.keys(), key=extract_number)


def extract_number(key):
    match = re.search(r"\d+", key)
    return int(match.group()) if match else float("inf")


def main():
    path = GetRootPart().Document.Path[:-5] + "stp"
    dict_of_bodies = get_dict_of_bodies()

    DocumentHelper.CreateNewDocument()
    for name in get_sorted_keys_by_number(dict_of_bodies):
        c = ComponentHelper.CreateAtRoot(name)
        ComponentHelper.SetActive(Selection.Create(c))
        sel = Selection.Create(dict_of_bodies[name])
        Copy.Execute(sel)
    options = ExportOptions.Create()
    DocumentSave.Execute(path, options)
    DocumentHelper.CloseDocument()


main()
