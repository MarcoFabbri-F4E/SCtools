# Python Script, API Version = V241
# type: ignore
# ruff: noqa: F821


def get_faces_with_toroidal_surfaces():
    faces_with_torus = []
    part = GetRootPart()
    bodies = part.GetAllBodies()
    for b in bodies:
        for f in b.Faces:
            if f.Shape.Geometry.GetType() == Torus:
                faces_with_torus.append(f)
    return faces_with_torus


def set_components_as_blue_transparent(comps):
    sel = Selection.Create(comps)
    options = SetColorOptions()
    options.FaceColorTarget = FaceColorTarget.Body
    ColorHelper.SetColor(sel, options, ColorHelper.Blue)
    ColorHelper.SetFillStyle(sel, FillStyle.Transparent)


def set_faces_as_red_opaque_and_body_yellow(faces):
    # bodies
    for face in faces:
        body = face.Parent
        sel = Selection.Create(body)
        options = SetColorOptions()
        options.FaceColorTarget = FaceColorTarget.Body
        ColorHelper.SetColor(sel, options, Color.Yellow)
        ColorHelper.SetFillStyle(sel, FillStyle.Opaque)
    # faces
    sel = Selection.Create(faces)
    options = SetColorOptions()
    options.EdgeColorTarget = EdgeColorTarget.Body
    options.FaceColorTarget = FaceColorTarget.Face
    ColorHelper.SetColor(sel, options, Color.Red)
    ColorHelper.SetFillStyle(sel, FillStyle.Opaque)


def main():
    faces = get_faces_with_toroidal_surfaces()
    if len(faces) == 0:
        MessageBox.Show("No toroidal surfaces found!")
        return

    set_components_as_blue_transparent(GetRootPart())
    set_faces_as_red_opaque_and_body_yellow(faces)


main()
