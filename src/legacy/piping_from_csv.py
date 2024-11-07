# Python Script, API Version = V241
# type: ignore
# ruff: noqa: F821
from math import acos, cos, pi, sin, tan
from re import sub


class p_component:
    """
    This class contains the information to generate a piping component, which
    may be composed of several bodys. Each body consists on one or two cylinders
    and two planes.
    """

    def __init__(self, infile, line):
        self.infile = infile
        self.X = []
        self.Y = []
        self.Z = []
        self.BR = []  # This list contains n-2 bend radius
        self.populate(line)
        self.r = (
            self.R / 2
        )  # Provisional value of the minus radius until it is included in the csv

    def populate(self, line):
        """
        Reads the csv parsing the information of the current component.
        """
        self.Part_Number = line[i_PN]
        self.R = float(line[i_SD]) / 2  # Major radius in mm
        while len(line) > 1:
            self.X.append(line[i_X])
            self.Y.append(line[i_Y])
            self.Z.append(line[i_Z])
            BR = line[i_BR]
            if BR != "\n":
                self.BR.append(float(BR[:-1]))
            line = self.infile.readline().split(",")
            if line[0] != "":
                break
        self.next_line = line


def parse_csv(csv_name):
    """
    Returns a list of components.
    """
    global i_X, i_Y, i_Z, i_PN, i_SD, i_BR
    with open(csv_name, "r") as infile:
        comp_list = []
        line = infile.readline().split(",")
        for i, v in enumerate(line):
            if "X" in v:
                i_X = i
            elif "Y" in v:
                i_Y = i
            elif "Z" in v:
                i_Z = i
            elif "Part Number" in v:
                i_PN = i
            elif "Section Diameter" in v:
                i_SD = i
            elif "BendRadius" in v:
                i_BR = i

        line = infile.readline().split(",")
        while len(line) > 1:
            p = p_component(infile, line)
            line = p.next_line
            if len(p.X) > 1:
                comp_list.append(p)
        return comp_list


def Tubes_from_points(points, R):
    p1 = points[0]
    p2 = points[1]
    v12 = [p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2]]
    P1 = Point.Create(MM(p1[0]), MM(p1[1]), MM(p1[2]))
    D12 = Direction.Create(v12[0], v12[1], v12[2])
    Plane0 = DatumPlaneCreator.Create(P1, D12).CreatedPlanes[0]
    for i in range(len(points) - 1):
        p1 = points[i]
        p2 = points[i + 1]
        P1 = Point.Create(MM(p1[0]), MM(p1[1]), MM(p1[2]))
        P2 = Point.Create(MM(p2[0]), MM(p2[1]), MM(p2[2]))
        v12 = [p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2]]
        v12mid = [v12[0] * 0.5, v12[1] * 0.5, v12[2] * 0.5]
        v12mod = (v12[0] ** 2 + v12[1] ** 2 + v12[2] ** 2) ** 0.5
        v12 = [v12[0] / v12mod, v12[1] / v12mod, v12[2] / v12mod]
        D12 = Direction.Create(v12[0], v12[1], v12[2])
        if i < len(points) - 2:
            p3 = points[i + 2]
            v23 = [p3[0] - p2[0], p3[1] - p2[1], p3[2] - p2[2]]
            v23mod = (v23[0] ** 2 + v23[1] ** 2 + v23[2] ** 2) ** 0.5
            v23 = [v23[0] / v23mod, v23[1] / v23mod, v23[2] / v23mod]
            D2 = [v12[0] + v23[0], v12[1] + v23[1], v12[2] + v23[2]]
            D2 = Direction.Create(D2[0], D2[1], D2[2])
            P2 = Point.Create(MM(p2[0]), MM(p2[1]), MM(p2[2]))
            Plane2 = DatumPlaneCreator.Create(P2, D2).CreatedPlanes[0]
        else:
            v23 = v12
            Plane2 = DatumPlaneCreator.Create(P2, D12).CreatedPlanes[0]

        pmid = [p1[0] + v12mid[0], p1[1] + v12mid[1], p1[2] + v12mid[2]]
        Pmid = Point.Create(MM(pmid[0]), MM(pmid[1]), MM(pmid[2]))
        Dmid = Direction.Create(v12[0], v12[1], v12[2])
        Plane1 = DatumPlaneCreator.Create(Pmid, Dmid).CreatedPlanes[0]

        sel = Selection.Create(Plane1)
        ViewHelper.SetSketchPlane(sel)
        S1 = SketchCircle.Create(Pmid, MM(R)).CreatedCurves[0]
        res = Fill.Execute(Selection.Create(S1))
        F1 = res.GetCreated[IDesignFace]()
        sel = Selection.Create(F1)
        upsel = Selection.Create(Plane0)
        options = ExtrudeFaceOptions()
        options.ExtrudeType = ExtrudeType.ForceIndependent
        ex1 = ExtrudeFaces.UpTo(sel, D12, upsel, P1, options)
        ex1 = ex1.CreatedBodies[0]

        res = Fill.Execute(Selection.Create(S1))
        F1 = res.GetCreated[IDesignFace]()
        sel = Selection.Create(F1)
        upsel = Selection.Create(Plane2)
        options = ExtrudeFaceOptions()
        options.ExtrudeType = ExtrudeType.ForceIndependent
        ex2 = ExtrudeFaces.UpTo(sel, D12, upsel, P2, options)
        ex2 = ex2.CreatedBodies[0]

        Delete.Execute(Selection.Create(S1))
        Delete.Execute(Selection.Create(Plane0))
        Delete.Execute(Selection.Create(Plane1))
        Plane0 = Plane2
        targets = Selection.Create(ex1, ex2)
        Combine.Merge(targets)
    Delete.Execute(Selection.Create(Plane0))
    sel = Selection.Create(GetRootPart().Bodies)
    hide(sel)


def show(sel):
    visibility = VisibilityType.Show
    inSelectedView = False
    ViewHelper.SetObjectVisibility(sel, visibility, inSelectedView)


def hide(sel):
    visibility = VisibilityType.Hide
    inSelectedView = False
    ViewHelper.SetObjectVisibility(sel, visibility, inSelectedView)


def find_arc_points(p1, p2, p3, r, n):
    v21 = (p1[0] - p2[0], p1[1] - p2[1], p1[2] - p2[2])
    v23 = (p3[0] - p2[0], p3[1] - p2[1], p3[2] - p2[2])

    vprod = v21[0] * v23[0] + v21[1] * v23[1] + v21[2] * v23[2]

    v1mod = (v21[0] ** 2 + v21[1] ** 2 + v21[2] ** 2) ** 0.5
    v2mod = (v23[0] ** 2 + v23[1] ** 2 + v23[2] ** 2) ** 0.5

    v21 = (v21[0] / v1mod, v21[1] / v1mod, v21[2] / v1mod)
    v23 = (v23[0] / v2mod, v23[1] / v2mod, v23[2] / v2mod)

    alpha = acos(vprod / (v1mod * v2mod)) * 0.5
    if pi - 2 * alpha < 0.001:
        return [p1, p3]
    if n == 0:
        return [p1, p2, p3]
    d = r / tan(alpha)

    ps = [p2[0] + d * v21[0], p2[1] + d * v21[1], p2[2] + d * v21[2]]
    pe = (p2[0] + d * v23[0], p2[1] + d * v23[1], p2[2] + d * v23[2])

    vcross = (
        v21[1] * v23[2] - v23[1] * v21[2],
        -v21[0] * v23[2] + v23[0] * v21[2],
        v21[0] * v23[1] - v23[0] * v21[1],
    )
    vcross_mod = (vcross[0] ** 2 + vcross[1] ** 2 + vcross[2] ** 2) ** 0.5
    vcross = (vcross[0] / vcross_mod, vcross[1] / vcross_mod, vcross[2] / vcross_mod)

    vc = (
        vcross[1] * v21[2] - v21[1] * vcross[2],
        -vcross[0] * v21[2] + v21[0] * vcross[2],
        vcross[0] * v21[1] - v21[0] * vcross[1],
    )
    vc_mod = (vc[0] ** 2 + vc[1] ** 2 + vc[2] ** 2) ** 0.5

    vc = (vc[0] / vc_mod, vc[1] / vc_mod, vc[2] / vc_mod)  # vec dir from ps to c
    vcs = (vc[0], vc[1], vc[2])

    c = (ps[0] + r * vc[0], ps[1] + r * vc[1], ps[2] + r * vc[2])

    vcs = (vcs[0] * -r, vcs[1] * -r, vcs[2] * -r)  # vec with dir equal to c to ps

    vcross = [-vcross[0], -vcross[1], -vcross[2]]

    points = [p1, ps]
    for i in range(n - 1):
        rot_ang = (pi - alpha * 2) / n * (i + 1)
        v_rotX = (
            (cos(rot_ang) + vcross[0] ** 2 * (1 - cos(rot_ang))) * vcs[0]
            + (vcross[0] * vcross[1] * (1 - cos(rot_ang)) - vcross[2] * sin(rot_ang))
            * vcs[1]
            + (vcross[0] * vcross[2] * (1 - cos(rot_ang)) + vcross[1] * sin(rot_ang))
            * vcs[2]
        )
        v_rotY = (
            (vcross[1] * vcross[0] * (1 - cos(rot_ang)) + vcross[2] * sin(rot_ang))
            * vcs[0]
            + (cos(rot_ang) + vcross[1] ** 2 * (1 - cos(rot_ang))) * vcs[1]
            + (vcross[1] * vcross[2] * (1 - cos(rot_ang)) - vcross[0] * sin(rot_ang))
            * vcs[2]
        )
        v_rotZ = (
            (vcross[0] * vcross[2] * (1 - cos(rot_ang)) - vcross[1] * sin(rot_ang))
            * vcs[0]
            + (vcross[1] * vcross[2] * (1 - cos(rot_ang)) + vcross[0] * sin(rot_ang))
            * vcs[1]
            + (cos(rot_ang) + vcross[2] ** 2 * (1 - cos(rot_ang))) * vcs[2]
        )

        p_i = [v_rotX + c[0], v_rotY + c[1], v_rotZ + c[2]]
        points.append(p_i)
    points.append(pe)
    points.append(p3)
    return points


#########################################################
n = 2  # Number of divisions per arc, if 0 then no arc

comps = parse_csv("pipes_small.csv")

for comp in comps:
    points = []
    for i in range(len(comp.X)):
        p = [comp.X[i], comp.Y[i], comp.Z[i]]
        p = [float(i.split()[0]) for i in p]  # assuming they are in mm
        points.append(p)
    # Now we modify the points list to add the arc points
    new_points = []
    iterations = len(points) - 2
    for i in range(iterations):
        BR = float(comp.BR[i])
        new = find_arc_points(points.pop(0), points.pop(0), points.pop(0), BR, n)
        new_points = new_points[:-2] + new
        points = new_points[-2:] + points
    if len(new_points) > 0:
        points = new_points

    name = comp.Part_Number
    name = sub("\s", "", name)
    try:
        Tubes_from_points(points, comp.R)
        Tubes_from_points(points, comp.r)

        sel = Selection.Create(GetRootPart().Bodies)
        show(sel)
        result = FixInterference.FindAndFix()

        leng = len(GetRootPart().Bodies) / 2
        sel_t = Selection.Create(GetRootPart().Bodies[:leng])
        res = ComponentHelper.MoveBodiesToComponent(sel_t)
        GetRootPart().Components[-1].SetName(name)
        sel_w = Selection.Create(GetRootPart().Bodies)
        res = ComponentHelper.MoveBodiesToComponent(sel_w)
        GetRootPart().Components[-1].SetName("WATER_" + name)
        sel = Selection.Create(GetRootPart().Components[-1])
        options = SetColorOptions()
        options.UseAlpha = False
        options.FaceColorTarget = FaceColorTarget.Body
        ColorHelper.SetColor(sel, options, Color.DeepSkyBlue)
        sel = Selection.Create(GetRootPart().GetAllBodies())
        hide(sel)
    except:
        sel = Selection.Create(GetRootPart())
        ComponentHelper.CreateNewComponent(sel)
        ComponentHelper.SetRootActive(None)
        GetRootPart().Components[-1].SetName("FAILED-" + name)
        sel = Selection.Create(GetRootPart().Bodies)
        Delete.Execute(sel)
        sel = Selection.Create(GetRootPart().DatumPlanes)
        Delete.Execute(sel)
        sel = Selection.Create(GetRootPart().Curves)
        Delete.Execute(sel)

mode = InteractionMode.Solid
result = ViewHelper.SetViewMode(mode)
