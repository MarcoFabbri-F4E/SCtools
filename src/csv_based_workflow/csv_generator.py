# Python Script, API Version = V241
# type: ignore
# ruff: noqa: F821
# ruff: noqa: UP032
import csv
import os
import re
from copy import deepcopy


class CSVGenerator:
    def __init__(self):
        self.csv_file_path = GetRootPart().Document.Path[:-6] + ".csv"
        self.dict_components = self.get_dict_from_spaceclaim()

    class Row:
        def __init__(self, tree, material_info, number_of_bodies, volume_info, comment):
            self.tree = tree  # e.g. ["Assembly1", "ComponentXYZ"]
            self.material_info = material_info
            self.number_of_bodies = number_of_bodies
            self.volume_info = volume_info
            self.comment = comment

        class MaterialInfo:
            def __init__(self, name=None, density=None, mass=None):
                self.name = name
                self.density = density
                self.mass = mass

        class VolumeInfo:
            def __init__(
                self,
                original=None,
                difference=None,
                simplified=None,
                stochastic=None,
                density_correction_factor=None,
            ):
                self.original = original
                self.difference = difference
                self.simplified = simplified
                self.stochastic = stochastic
                self.density_correction_factor = density_correction_factor

        @classmethod
        def build_from_spaceclaim_component(cls, component):
            tree = cls.get_tree_from_component(component)
            material_info = cls.MaterialInfo()
            bodies = [b for b in component.GetBodies() if b.Shape.Volume > 0.0]
            volume_original = sum(b.MassProperties.Mass for b in bodies)
            volume_original *= 1000000  # To make it cm3
            volume_info = cls.VolumeInfo(original=volume_original)
            number_of_bodies = len(bodies)
            comment = None

            return cls(tree, material_info, number_of_bodies, volume_info, comment)

        @classmethod
        def build_from_csv_row(cls, csv_row):
            tree = cls.get_tree_from_csv_row(csv_row)
            material = csv_row["MATERIAL"]
            mass = cls.float_or_none(csv_row["MASS [g]"])
            density = cls.float_or_none(csv_row["DENSITY [g/cm3]"])
            number_of_bodies = cls.get_number_of_bodies(csv_row["CELL IDs"])
            volume_original = cls.float_or_none(csv_row["ORIGINAL VOLUME [cm3]"])
            volume_difference = cls.float_or_none(csv_row["%dif (ORG-SIM)/ORG*100"])
            volume_simplified = cls.float_or_none(csv_row["SIMPLIFIED VOLUME"])
            volume_stochastic = cls.float_or_none(csv_row["STOCHASTIC VOLUME"])
            density_correction_factor = cls.float_or_none(csv_row["DCF=ORG/STOCH"])
            comment = csv_row["COMMENT"]

            material_info = cls.MaterialInfo(material, density, mass)
            volume_info = cls.VolumeInfo(
                volume_original,
                volume_difference,
                volume_simplified,
                volume_stochastic,
                density_correction_factor,
            )
            return cls(tree, material_info, number_of_bodies, volume_info, comment)

        @staticmethod
        def get_tree_from_component(component):
            tree = []
            while True:
                try:
                    tree.insert(0, component.GetName())
                    component = component.Parent.Parent
                except AttributeError:
                    return tree

        @staticmethod
        def get_tree_from_csv_row(row):
            tree = []
            i = 0
            while True:
                try:
                    tree.append(row["Level " + str(i)])
                    i += 1
                except KeyError:
                    return tree + [row["Component ID"]]

        @staticmethod
        def get_number_of_bodies(value):
            try:
                id_0 = int(value.split()[0][1:-1])
                id_1 = int(value.split()[-1][:-1])
                return id_1 - id_0 + 1
            except (ValueError, IndexError):
                return None

        @staticmethod
        def float_or_none(value):
            try:
                return float(value)
            except ValueError:
                return None

    def get_dict_from_spaceclaim(self):
        list_components = self.get_all_components_with_bodies()
        dict_components = {}
        for comp in list_components:
            name = comp.GetName()
            if not re.match(r"Component\d+", name):
                MessageBox.Show(name + " does not follow ComponentXXX convention!")
            if name in dict_components:
                MessageBox.Show(name + " is repeated!")
            dict_components[name] = self.Row.build_from_spaceclaim_component(comp)
        return dict_components

    @staticmethod
    def get_all_components_with_bodies():
        selected_comps = []

        components = GetRootPart().GetAllComponents()
        for comp in components:
            bodies = comp.GetBodies()
            if len(bodies) > 0:
                selected_comps.append(comp)

        return selected_comps

    def get_dict_from_csv(self):
        result_dict = {}
        with open(self.csv_file_path) as infile:
            reader = csv.DictReader(infile)
            tree_length = 0
            for row in reader:
                if tree_length == 0:
                    levels = [key for key in row.keys() if "Level" in key]
                    tree_length = len(levels)

                result_dict[row["Component ID"]] = self.Row.build_from_csv_row(row)

        return result_dict

    def generate_csv(self):
        if os.path.exists(self.csv_file_path):
            dict_from_csv = self.get_dict_from_csv()
            self.dict_components = self.compare_dicts(dict_from_csv)

        writer = Writer(self.dict_components, self.csv_file_path)
        writer.write_csv()

    def compare_dicts(self, dict_csv):
        combined_dict = deepcopy(dict_csv)
        for key in dict_csv.keys():
            combined_comp = combined_dict[key]

            if key in self.dict_components:
                spaceclaim_comp = self.dict_components[key]

                combined_comp.number_of_bodies = spaceclaim_comp.number_of_bodies

                volume_info = combined_comp.volume_info
                volume_info.simplified = spaceclaim_comp.volume_info.original
                volume_info.difference = (
                    (volume_info.original - volume_info.simplified)
                    / volume_info.original
                    * 100
                )
                volume_info.difference = "{:.3f}".format(volume_info.difference)

                combined_comp.tree = spaceclaim_comp.tree
            else:
                combined_comp.number_of_bodies = "DELETED"
                combined_comp.volume_info.difference = ""
                combined_comp.volume_info.simplified = ""

        for key in self.dict_components.keys():
            if key not in dict_csv:
                combined_dict[key] = self.dict_components[key]

        return combined_dict


class Writer:
    def __init__(self, dict_components, csv_file_path):
        self.dict_components = dict_components
        self.csv_file_path = csv_file_path
        self.tree_length = self.get_tree_length_from_dict(dict_components)
        self.cell_id = 1

    def write_csv(self):
        columns = ["Level {}".format(i) for i in range(self.tree_length - 1)]
        columns += [
            "Component ID",
            "MATERIAL",
            "MASS [g]",
            "DENSITY [g/cm3]",
            "CELL IDs",
            "ORIGINAL VOLUME [cm3]",
            "%dif (ORG-SIM)/ORG*100",
            "SIMPLIFIED VOLUME",
            "STOCHASTIC VOLUME",
            "DCF=ORG/STOCH",
            "COMMENT",
        ]
        with open(self.csv_file_path, "wb") as infile:
            csv_writer = csv.DictWriter(infile, fieldnames=columns)
            csv_writer.writeheader()
            for name in self.get_sorted_keys_by_number():
                self.write_row(csv_writer, name)

    def write_row(self, csv_writer, name):
        row = self.dict_components[name]
        if row.number_of_bodies == "DELETED":
            cell_ids = "DELETED"
        else:
            cell_ids = [self.cell_id, self.cell_id + row.number_of_bodies - 1]
            self.cell_id += row.number_of_bodies

        tree = deepcopy(row.tree)
        name = tree.pop(-1)

        while len(tree) < self.tree_length:
            tree.append("-")
        write_dict = {
            "Level {}".format(i): tree[i] for i in range(self.tree_length - 1)
        }
        write_dict["Component ID"] = name
        write_dict["MATERIAL"] = str(row.material_info.name)
        write_dict["MASS [g]"] = str(row.material_info.mass)
        write_dict["DENSITY [g/cm3]"] = str(row.material_info.density)
        write_dict["CELL IDs"] = str(cell_ids)
        write_dict["ORIGINAL VOLUME [cm3]"] = str(row.volume_info.original)
        write_dict["%dif (ORG-SIM)/ORG*100"] = str(row.volume_info.difference)
        write_dict["SIMPLIFIED VOLUME"] = str(row.volume_info.simplified)
        write_dict["STOCHASTIC VOLUME"] = str(row.volume_info.stochastic)
        write_dict["DCF=ORG/STOCH"] = str(row.volume_info.density_correction_factor)
        write_dict["COMMENT"] = str(row.comment)

        for key in write_dict.keys():
            if write_dict[key] == "None":
                write_dict[key] = ""

        csv_writer.writerow(write_dict)

    @staticmethod
    def get_tree_length_from_dict(dict_components):
        tree_length = 0
        for row in dict_components.values():
            tree_length = max(len(row.tree), tree_length)
        return tree_length

    def get_sorted_keys_by_number(self):
        return sorted(self.dict_components.keys(), key=self.extract_number)

    @staticmethod
    def extract_number(key):
        match = re.search(r"\d+", key)
        return int(match.group()) if match else float("inf")


def main():
    csv_generator = CSVGenerator()
    csv_generator.generate_csv()


main()
