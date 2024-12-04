# Python Script, API Version = V241
# type: ignore
# ruff: noqa: F821
# ruff: noqa: UP032
"""
Select a body and run the script to get its FMESH and TR cards.
The body should be a prism: 6 reactangular and orthogonal faces
"""


def main():
    body = Selection.GetActive().Items[0]
    check_is_hexaedron(body)

    bottom_left_point = get_bottom_left_point(body)
    unordered_axes = get_unordered_axes(body, bottom_left_point)
    axes = order_axes_as_xyz(unordered_axes, bottom_left_point)
    vectors = convert_edges_to_vectors(axes, bottom_left_point)

    imesh, jmesh, kmesh = (vec.Magnitude * 100 for vec in vectors)
    matrix = [normalize(vec) for vec in vectors]
    bottom_left_point_cm = bottom_left_point * 100
    matrix.insert(0, bottom_left_point_cm)

    print_cards(imesh, jmesh, kmesh, matrix)


def check_is_hexaedron(body):
    number_of_faces_in_hexaedron = 6
    if len(body.Faces) != number_of_faces_in_hexaedron:
        MessageBox.Show("The body doesnt have 6 surfaces")
        raise AssertionError()

    for face in body.Faces:
        if type(face.Shape.Geometry) is not Plane:
            MessageBox.Show("The surfaces are not all Planes")
            raise AssertionError()


def get_bottom_left_point(body):
    edges = body.Edges
    edge = edges[0]
    bottom_left_1 = edge.EvalStart().Point
    for edge in edges:
        for point in (edge.EvalStart().Point, edge.EvalEnd().Point):
            if get_xy_combination(point) < get_xy_combination(bottom_left_1):
                bottom_left_1 = point
    bottom_left_2 = edge.EvalEnd().Point
    for edge in edges:
        for point in (edge.EvalStart().Point, edge.EvalEnd().Point):
            if point == bottom_left_1:
                continue
            if get_xy_combination(point) < get_xy_combination(bottom_left_2):
                bottom_left_2 = point

    if bottom_left_1.Z < bottom_left_2.Z:
        return bottom_left_1
    return bottom_left_2


def get_xy_combination(point):
    return point.X + point.Y


def get_unordered_axes(body, bottom_left_point):
    edges = body.Edges
    axes = []
    for edge in edges:
        for point in (edge.EvalStart().Point, edge.EvalEnd().Point):
            if point == bottom_left_point:
                axes.append(edge)
    return axes


def order_axes_as_xyz(unordered_axes, bottom_left_point):
    x_axis = unordered_axes[0]
    for axis in unordered_axes:
        if (
            get_other_point_from_edge(axis, bottom_left_point).X
            > get_other_point_from_edge(x_axis, bottom_left_point).X
        ):
            x_axis = axis
    y_axis = unordered_axes[0]
    for axis in unordered_axes:
        if (
            get_other_point_from_edge(axis, bottom_left_point).Y
            > get_other_point_from_edge(y_axis, bottom_left_point).Y
        ):
            y_axis = axis
    z_axis = unordered_axes[0]
    for axis in unordered_axes:
        if (
            get_other_point_from_edge(axis, bottom_left_point).Z
            > get_other_point_from_edge(z_axis, bottom_left_point).Z
        ):
            z_axis = axis
    return [x_axis, y_axis, z_axis]


def get_other_point_from_edge(edge, point):
    if edge.EvalStart().Point == point:
        return edge.EvalEnd().Point
    return edge.EvalStart().Point


def convert_edges_to_vectors(axes, bottom_left_point):
    vectors = []
    for axis in axes:
        vectors.append(
            get_other_point_from_edge(axis, bottom_left_point) - bottom_left_point
        )
    return vectors


def normalize(vec):
    return vec / vec.Magnitude


def print_cards(imesh, jmesh, kmesh, matrix):
    text = "TR1 \n"
    for vector in matrix:
        text += "     {:.4f} {:.4f} {:.4f} \n".format(vector[0], vector[1], vector[2])

    text += "FMESH4:n  \n"
    text += "     imesh {:.2f} iints 10 \n".format(imesh)
    text += "     jmesh {:.2f} jints 10 \n".format(jmesh)
    text += "     kmesh {:.2f} kints 10 \n".format(kmesh)

    text += "     tr=1"

    print(text)


main()
