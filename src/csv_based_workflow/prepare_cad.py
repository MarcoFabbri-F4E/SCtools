# Python Script, API Version = V241
# type: ignore
# ruff: noqa: F821


class ComponentData:
    comp_id = 1

    def __init__(self, comp):
        self.name = comp.GetName().Trim()
        self.bodies = comp.GetBodies()
        self.subcomps_data = []
        for subcomp in comp.GetComponents():
            self.subcomps_data.append(ComponentData(subcomp))

    def regenerate_via_body_pasting(self, ancestor_comp=None):
        # create comp
        if ancestor_comp is None:
            ComponentHelper.CreateAtRoot(self.name)
            current_comp = GetRootPart().GetComponents()[-1]
        else:
            ComponentHelper.CreateAtComponent(ancestor_comp, self.name)
            current_comp = ComponentHelper.GetActive().GetComponents()[-1]

        # paste bodies in new ComponentXXX
        if len(self.bodies) > 0:
            ComponentHelper.CreateAtComponent(
                current_comp, "Component" + str(ComponentData.comp_id)
            )
            ComponentData.comp_id += 1
            ComponentHelper.SetActive(current_comp.GetComponents()[-1])
            Copy.Execute(Selection.Create(self.bodies))

        # repeat for subcomps
        for subcomp_data in self.subcomps_data:
            ComponentHelper.SetActive(current_comp)
            subcomp_data.regenerate_via_body_pasting(current_comp)


def main():
    path = GetRootPart().Document.Path[:-6] + "_INDEPENDENT.scdoc"
    root_comp_data = ComponentData(GetRootPart())
    DocumentHelper.CreateNewDocument()
    root_comp_data.regenerate_via_body_pasting()
    ComponentHelper.SetRootActive()
    DocumentSave.Execute(path)
    DocumentHelper.CloseDocument()


main()
