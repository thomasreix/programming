def generate_face(iteration):
    width = 3**iteration
    face_points = [(0, 0), (width, 0), (width, 1), (1, 1)]
    x, y = 1, 1
    for i in range(iteration):
        cornerA = (x + i, y + i + 1)
        face_points.append(cornerA)
        cornerB = (x + i + 1, y + i + 1)
        face_points.append(cornerB)
        cornerC = (x + i + 1, y + i)
        face_points.append(cornerC)

    face_points.append((width, 1))
    face_points.append((width, width))
    face_points.append((0, width))

    return face_points


def map_points(points, offset_x, offset_y, size, angle_x, angle_y):
    mapped_points = []
    for point in points:
        point_x, point_y = point
        mapped_point_x = point_x * size + offset_x + (point_y * angle_x)
        mapped_point_y = point_y * size + offset_y + (point_x * angle_y)
        mapped_point = (mapped_point_x, mapped_point_y)
        mapped_points.append(mapped_point)

    return mapped_points


def draw_face(points, color, stroke_color, stroke_width):
    points_string = ""

    for point in points:
        x = point[0]
        y = point[1]
        points_string += f"{x},{y} "

    face = f"""<polygon
        points="{points_string}"
        fill="{color}"
        stroke="{stroke_color}"
        stroke-width="{stroke_width}"/>
"""

    return face


def generate_svg(poligons):
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg"
    width="800"
    height="600"
    viewBox="0 0 800 600"
    style="background-color: #0f0f0f;">

"""

    for poligon in poligons:
        svg += f"   {poligon}\n"

    svg += "</svg>"
    with open("menger-sponge.svg", "w") as file:
        file.write(svg)


def main():
    up_color = "#f7f7ff"
    left_color = "#c8c7ff"
    right_color = "#9491ff"

    stroke_color = "#625fd7"
    stroke_width = 2

    iteration = 1

    face_points = generate_face(iteration)

    face_x, face_y = 200, 200
    size = 100
    angle_x, angle_y = 2, 30
    mapped_points = map_points(face_points, face_x, face_y, size, angle_x, angle_y)

    face = draw_face(mapped_points, left_color, stroke_color, stroke_width)

    poligons = [face]
    generate_svg(poligons)


if __name__ == "__main__":
    main()
