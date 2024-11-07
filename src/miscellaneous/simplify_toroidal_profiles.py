# Python Script, API Version = V241
# type: ignore
# ruff: noqa: F821
import math

STEP_ANGLE = 10
EPSILON = 1e-5


def normalize(v):
    norm = math.sqrt(sum(x**2 for x in v))
    return tuple(x / norm for x in v)


def distance(p1, p2):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(p1, p2)))


def vector_from_to(from_point, to_point):
    return tuple(to_point[i] - from_point[i] for i in range(3))


def dot_product(v1, v2):
    return sum(x * y for x, y in zip(v1, v2))


def angle_between_vectors(v1, v2, normal):
    # Assuming v1 and v2 are in the same plane and normalized
    angle = math.atan2(dot_product(cross_product(v1, v2), normal), dot_product(v1, v2))
    return angle


def cross_product(v1, v2):
    return (
        v1[1] * v2[2] - v1[2] * v2[1],
        v1[2] * v2[0] - v1[0] * v2[2],
        v1[0] * v2[1] - v1[1] * v2[0],
    )


def rotate_vector(vector, axis, angle):
    axis = normalize(axis)
    x, y, z = vector
    u, v, w = axis
    cos_angle = math.cos(angle)
    sin_angle = math.sin(angle)

    dot_prod = dot_product(vector, axis)
    cross_prod = cross_product(axis, vector)
    rotated_vector = (
        u * dot_prod * (1 - cos_angle) + x * cos_angle + cross_prod[0] * sin_angle,
        v * dot_prod * (1 - cos_angle) + y * cos_angle + cross_prod[1] * sin_angle,
        w * dot_prod * (1 - cos_angle) + z * cos_angle + cross_prod[2] * sin_angle,
    )
    return rotated_vector


def calculate_intermediate_points(center, start_point, end_point, normal, degrees_step):
    normal = normalize(normal)
    radius = distance(center, start_point)

    current_vector = normalize(vector_from_to(center, start_point))
    end_vector = normalize(vector_from_to(center, end_point))

    intermediate_points = [
        tuple(center[i] + current_vector[i] * radius for i in range(3))
    ]
    while angle_between_vectors(current_vector, end_vector, normal) > EPSILON:
        angle = math.radians(degrees_step)
        rotated_vector = rotate_vector(current_vector, normal, angle)
        intermediate_point = tuple(
            center[i] + rotated_vector[i] * radius for i in range(3)
        )
        intermediate_points.append(intermediate_point)
        current_vector = rotated_vector

    intermediate_points[-1] = tuple(
        center[i] + end_vector[i] * radius for i in range(3)
    )

    return intermediate_points


def get_circle_parameters(line):
    start = list(line.Shape.StartPoint)
    end = list(line.Shape.EndPoint)
    center = list(line.Shape.Geometry.Axis.Origin)
    normal = list(line.Shape.Geometry.Axis.Direction)
    return center, start, end, normal


def main():
    selection = Selection.GetActive()
    lines = selection.Items
    for line in lines:
        if line.Shape.Geometry.GetType() == Circle:
            center, start, end, normal = get_circle_parameters(line)
            points = calculate_intermediate_points(
                center, start, end, normal, STEP_ANGLE
            )
            points = [Point.Create(p[0], p[1], p[2]) for p in points]
            SketchLine.CreateChain(points)
        elif line.Shape.Geometry.GetType() == Line:
            SketchLine.Create(line.Shape.StartPoint, line.Shape.EndPoint)
    Delete.Execute(selection)


main()
