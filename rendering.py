from dataclasses import dataclass
from math import cos, sin, pi, sqrt

import pygame
from pygame import Surface

import sys


@dataclass
class Dimension:
    scale: float
    width: float


@dataclass
class Color:
    vertex: tuple
    edge: tuple
    face: tuple


@dataclass
class Visibility:
    vertex: bool
    edge: bool
    face: bool


def get_shapes():
    disk_precision = 100
    disk_vertices = [[0, 0, 0]]
    for i in range(disk_precision):
        theta = 2 * pi / disk_precision * i
        x = cos(theta)
        y = sin(theta)
        disk_vertices.append([x, y, 0])

    disk_edges = []
    disk_faces = []
    for i in range(1, disk_precision):
        disk_faces.append([0, i, i + 1])
    disk_faces.append([0, disk_precision, 1])

    golden_ratio = (1 + sqrt(5)) / 2

    dodecahedron_vertices = [
        [1, 1, 1],
        [1, -1, 1],
        [1, 1, -1],
        [1, -1, -1],
        [-1, 1, 1],
        [-1, -1, 1],
        [-1, 1, -1],
        [-1, -1, -1],
        [golden_ratio, 0, 1 / golden_ratio],
        [golden_ratio, 0, -1 / golden_ratio],
        [1 / golden_ratio, golden_ratio, 0],
        [-1 / golden_ratio, golden_ratio, 0],
        [0, 1 / golden_ratio, golden_ratio],
        [0, -1 / golden_ratio, golden_ratio],
        [-golden_ratio, 0, 1 / golden_ratio],
        [-golden_ratio, 0, -1 / golden_ratio],
        [1 / golden_ratio, -golden_ratio, 0],
        [-1 / golden_ratio, -golden_ratio, 0],
        [0, 1 / golden_ratio, -golden_ratio],
        [0, -1 / golden_ratio, -golden_ratio],
    ]

    dodecahedron_edges = [
        [0, 8],
        [1, 8],
        [2, 9],
        [3, 9],
        [8, 9],
        [0, 10],
        [2, 10],
        [4, 11],
        [6, 11],
        [10, 11],
        [0, 12],
        [4, 12],
        [1, 13],
        [5, 13],
        [12, 13],
        [4, 14],
        [5, 14],
        [6, 15],
        [7, 15],
        [14, 15],
        [1, 16],
        [3, 16],
        [5, 17],
        [7, 17],
        [16, 17],
        [2, 18],
        [6, 18],
        [3, 19],
        [7, 19],
        [18, 19],
    ]

    dodecahedron_faces = [
        [10, 2, 9, 8, 0],
        [0, 8, 1, 13, 12],
        [2, 9, 3, 19, 18],
        [4, 11, 6, 15, 14],
        [10, 11, 6, 18, 2],
        [4, 12, 13, 5, 14],
        [7, 15, 14, 5, 17],
        [1, 16, 3, 9, 8],
        [16, 17, 5, 13, 1],
        [19, 7, 17, 16, 3],
        [18, 19, 7, 15, 6],
    ]

    # Generate mobius strip
    mobius_precision = 100
    mobius_vertices = []
    mobius_edges = []

    for i in range(mobius_precision):
        theta = 2 * pi / mobius_precision * i
        x = cos(theta) - 0.25 * cos(theta / 2) * cos(theta)
        y = sin(theta) - 0.25 * cos(theta / 2) * sin(theta)
        z = 0.25 * sin(theta / 2)
        mobius_vertices.append([x, y, z])

        x = cos(theta) + 0.25 * cos(theta / 2) * cos(theta)
        y = sin(theta) + 0.25 * cos(theta / 2) * sin(theta)
        z = -0.25 * sin(theta / 2)
        mobius_vertices.append([x, y, z])

        mobius_edges.append([2 * i, 2 * i + 1])

    mobius_faces = []
    for i in range(mobius_precision - 1):
        mobius_faces.append([i * 2, i * 2 + 1, i * 2 + 3, i * 2 + 2])
    mobius_faces.append([mobius_precision * 2 - 2, mobius_precision * 2 - 1, 1, 0])

    shapes = {
        "cube": {
            "vertices": [
                [1, 1, 1],
                [1, -1, 1],
                [-1, -1, 1],
                [-1, 1, 1],
                [1, 1, -1],
                [1, -1, -1],
                [-1, -1, -1],
                [-1, 1, -1],
            ],
            "edges": [
                [0, 1],
                [1, 2],
                [2, 3],
                [3, 0],
                [4, 5],
                [5, 6],
                [6, 7],
                [7, 4],
                [4, 0],
                [5, 1],
                [6, 2],
                [7, 3],
            ],
            "faces": [
                [0, 1, 2, 3],
                [4, 5, 6, 7],
                [0, 1, 5, 4],
                [1, 2, 6, 5],
                [2, 3, 7, 6],
                [3, 0, 4, 7],
            ],
        },
        "tetrahedron": {
            "vertices": [
                [1, 1, 1],
                [1, -1, -1],
                [-1, 1, -1],
                [-1, -1, 1],
            ],
            "edges": [
                [0, 1],
                [1, 2],
                [2, 3],
                [3, 0],
                [0, 2],
                [1, 3],
            ],
            "faces": [
                [0, 1, 2],
                [0, 1, 3],
                [0, 3, 2],
                [1, 2, 3],
            ],
        },
        "disk": {"vertices": disk_vertices, "edges": disk_edges, "faces": disk_faces},
        "dodecahedron": {
            "vertices": dodecahedron_vertices,
            "edges": dodecahedron_edges,
            "faces": dodecahedron_faces,
        },
        "mobius_strip": {
            "vertices": mobius_vertices,
            "edges": mobius_edges,
            "faces": mobius_faces,
        },
    }

    return shapes


def matrix_multiplication(
    matrix: list[list[float]], vector: list[float]
) -> list[float]:
    result = []
    for row in matrix:
        total = sum(row[i] * vector[i] for i in range(len(vector)))
        result.append(total)
    return result


def rotate_points(
    vertices: list[float],
    orientation: list,
):
    rotation_x = [
        [1, 0, 0],
        [0, cos(orientation[0]), -sin(orientation[0])],
        [0, sin(orientation[0]), cos(orientation[0])],
    ]
    rotation_y = [
        [cos(orientation[1]), 0, sin(orientation[1])],
        [0, 1, 0],
        [-sin(orientation[1]), 0, cos(orientation[1])],
    ]

    rotation_z = [
        [cos(orientation[2]), -sin(orientation[2]), 0],
        [sin(orientation[2]), cos(orientation[2]), 0],
        [0, 0, 1],
    ]

    rotated_points = []
    for vertex in vertices:
        rotate_x = matrix_multiplication(rotation_x, vertex)
        rotate_y = matrix_multiplication(rotation_y, rotate_x)
        rotate_z = matrix_multiplication(rotation_z, rotate_y)
        rotated_point = rotate_z
        rotated_points.append(rotated_point)

    return rotated_points


def project_points(vertices: list[list[float]]):
    projected_points = []
    distance = 4  # move the object away from the camera

    for vertex in vertices:
        x = vertex[0]
        y = vertex[1]
        z = vertex[2] + distance

        if z != 0:
            x = x / z
            y = y / z

        point = [x, y]
        projected_points.append(point)

    return projected_points


def display(
    screen: Surface,
    points: list[list[int]],
    edges: list[list[int]],
    faces: list[list[int]],
    scale: int,
    width: int,
    height: int,
    line_width: int,
    color: Color,
    visibility: Visibility,
):
    displayed_points = []
    for point in points:
        x = point[0] * scale + width / 2
        y = point[1] * scale + height / 2
        displayed_point = [x, y]
        displayed_points.append(displayed_point)

    if visibility.face:
        for face in faces:
            face_points = []
            for point in face:
                face_points.append(displayed_points[point])
            pygame.draw.polygon(screen, color.face, (face_points), 0)

    if visibility.edge:
        for edge in edges:
            pygame.draw.line(
                screen,
                color.edge,
                displayed_points[edge[0]],
                displayed_points[edge[1]],
                line_width,
            )

    if visibility.vertex:
        for point in displayed_points:
            pygame.draw.circle(screen, color.vertex, point, line_width, 0)


def main():
    pygame.init()

    width, height = 960, 540
    pygame.display.set_caption("3D Shape Viewer")
    screen = pygame.display.set_mode((width, height))

    shapes = get_shapes()

    # "cube", "tetrahedron", "dodecahedron", "disk", "mobius_strip"
    shape_index = "cube"
    shape = shapes[shape_index]

    vertices = shape["vertices"]
    edges = shape["edges"]
    faces = shape["faces"]

    orientation = [0, 0, 0]

    scale = 200
    color = Color((0, 63, 255), (0, 63, 255), (0, 127, 255))
    line_width = 2
    visibility = Visibility(vertex=False, edge=True, face=True)

    clock = pygame.time.Clock()
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill((0, 0, 0))

        orientation[0] += 0.01
        orientation[1] += 0.02
        orientation[2] += 0.00

        rotated_points = rotate_points(vertices, orientation)
        projected_points = project_points(rotated_points)
        display(
            screen,
            projected_points,
            edges,
            faces,
            scale,
            width,
            height,
            line_width,
            color,
            visibility,
        )

        pygame.display.flip()


if __name__ == "__main__":
    main()
