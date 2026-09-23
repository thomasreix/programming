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


def draw_face(face_points, face_x, face_y, size, ratio, side, colors):
    if side is LEFT:
        for point in face_points:
            



    points_string = ""

    for point in points:
        x = point[0]
        y = point[1]
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
    ratio = [3, 4]
    side = LEFT

    face_points = generate_face(iteration)
    left_face = draw_face(face_points, face_x, face_y, size, ratio, side, colors)

    poligons = [left_face]
    generate_svg(poligons)


if __name__ == "__main__":
    main()
