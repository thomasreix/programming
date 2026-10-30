from math import cos, pi, sin, atan2

from svg_utils import map, render


def point_on_circle(center, angle, radius=1):
    point = (radius * cos(angle) + center[0], radius * sin(angle) + center[1])
    return point


def slope_angle(vertex, other_vertex):
    dx = other_vertex[0] - vertex[0]
    dy = other_vertex[1] - vertex[1]
    angle = atan2(dy, dx)
    return angle


def add_polygon(vertex, other_vertex, sides):
    polygon = [vertex, other_vertex]
    dx = other_vertex[0] - vertex[0]
    dy = other_vertex[1] - vertex[1]
    angle = 2 * pi / sides
    x, y = other_vertex
    for _ in range(sides - 2):
        dx, dy = (
            dx * cos(angle) - dy * sin(angle),
            dx * sin(angle) + dy * cos(angle),
        )
        x += dx
        y += dy
        polygon.append((x, y))
    return polygon


def find_neighbors(vertex, tiling):
    neighbors = []
    for polygon in tiling:
        sides = len(polygon)
        for i, other_vertex in enumerate(polygon):
            if other_vertex == vertex:
                past_vertex = polygon[(i - 1) % sides]
                next_vertex = polygon[(i + 1) % sides]
                for neighbor in [past_vertex, next_vertex]:
                    if neighbor not in neighbors:
                        neighbors.append(neighbor)
    return neighbors


def complete_vertex(vertex, tiling, configuration):
    neighbors = find_neighbors(vertex, tiling)
    past_angle, angle = 0, 0
    angles = []
    for neighbor in neighbors:
        angle = slope_angle(vertex, neighbor)
        angles.append(past_angle - angle)
    print(angles)
    other_vertex = point_on_circle(vertex, angle)
    for sides in configuration:
        polygon = add_polygon(vertex, other_vertex, sides)
        if polygon not in tiling:
            tiling.append(polygon)
        angle = slope_angle(vertex, other_vertex) + pi - pi * 2 / sides
        other_vertex = point_on_circle(vertex, angle)


def color(polygons):
    colors = [
        "#ffff0f",  # triangle
        "#ff0f0f",  # square
        "#ff6f0f",  # pentagon
        "#0f3f6f",  # hexagon
        "#ff3fcf",  # heptagon
        "#0f6f0f",  # octagon
    ]
    colored_polygons = []
    for polygon in polygons:
        sides = len(polygon)
        index = sides - 3
        if index < 0:
            continue
        color = colors[index]
        colored_polygon = [color]
        colored_polygon.extend(polygon)
        colored_polygons.append(colored_polygon)
    return colored_polygons


def main():
    configuration = [4, 8, 8]
    vertices = [(0, 0)]
    tiling = []
    complete_vertex(vertices[0], tiling, configuration)
    new_vertices = []
    for vertex in vertices:
        neighbors = find_neighbors(vertex, tiling)
        for neighbor in neighbors:
            new_vertices.append(neighbor)
    for vertex in new_vertices:
        print(vertex)
        complete_vertex(vertex, tiling, configuration)

    tiling = color(tiling)
    tiling = map(tiling, 50, (200, 200))
    render(tiling, "tiling", True)


if __name__ == "__main__":
    main()
