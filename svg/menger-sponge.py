UP = 0
LEFT = 1
RIGHT = 2


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


def map_points(points, face_x, face_y, size, ratio, side):
    mapped_points = []
    lenth = points[1][0]
    if side is LEFT:
        for point in points:
            point_x = point[0]
            point_y = point[1]
            mapped_point_x = point_x / lenth * ratio[0] * size + face_x
            mapped_point_y = (point_y + point_x / lenth) / lenth * ratio[
                1
            ] * size + face_y
            mapped_point = (mapped_point_x, mapped_point_y)
            mapped_points.append(mapped_point)
    elif side is RIGHT:
        for point in points:
            point_x = -point[0]
            point_y = point[1]
            mapped_point_x = (
                (point_x / lenth * ratio[2] * size) + ratio[0] * size + ratio[2] * size + face_x
            )
            mapped_point_y = (point_y - point_x / lenth) / lenth * ratio[
                1
            ] * size + face_y
            mapped_point = (mapped_point_x, mapped_point_y)
            mapped_points.append(mapped_point)

    return mapped_points


def draw_face(face_points, face_x, face_y, size, ratio, side, colors):
    mapped_points = map_points(face_points, face_x, face_y, size, ratio, side)

    points_string = ""
    color = colors[side]

    for mapped_point in mapped_points:
        x = mapped_point[0]
        y = mapped_point[1]
        points_string += f"{x},{y} "

    face = f"""<polygon
        points="{points_string}"
        fill="{color}"
        stroke-width="0"/>
"""

    return face


def generate_svg(poligons):
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg"
    width="800"
    height="600"
    viewBox="0 0 800 600">

"""

    for poligon in poligons:
        svg += f"   {poligon}\n"

    svg += "</svg>"
    with open("menger-sponge.svg", "w") as file:
        file.write(svg)


def main():
    up_color = "#ff0000"
    left_color = "#00ff00"
    right_color = "#0000ff"
    colors = [up_color, left_color, right_color]

    iteration = 1
    face_x, face_y = 100, 100
    size = 50
    ratio = [3, 4, 3]
    side = LEFT

    face_points = generate_face(iteration)
    left_face = draw_face(face_points, face_x, face_y, size, ratio, side, colors)

    side = RIGHT
    face_points = generate_face(iteration)
    right_face = draw_face(face_points, face_x, face_y, size, ratio, side, colors)

    poligons = [left_face, right_face]
    generate_svg(poligons)


if __name__ == "__main__":
    main()
