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
    if side is UP:
        for point in points:
            x, y = point

            x_ratio = x / lenth
            y_ratio = y / lenth

            mapped_point_x = (
                x_ratio * ratio[0] * size + y_ratio * ratio[2] * size + face_x
            )

            mapped_point_y = (
                x_ratio * ratio[1] * size / lenth
                - y_ratio * ratio[1] * size / lenth
                + face_y
            )

            mapped_points.append((mapped_point_x, mapped_point_y))

    elif side is LEFT:
        for point in points:
            x = point[0]
            y = point[1]
            mapped_point_x = x / lenth * ratio[0] * size + face_x
            mapped_point_y = (y + x / lenth) / lenth * ratio[1] * size + face_y
            mapped_point = (mapped_point_x, mapped_point_y)
            mapped_points.append(mapped_point)
    else:  # RIGHT:
        for point in points:
            x = -point[0]
            y = point[1]
            mapped_point_x = (
                (x / lenth * ratio[2] * size)
                + ratio[0] * size
                + ratio[2] * size
                + face_x
            )
            mapped_point_y = (y - x / lenth) / lenth * ratio[1] * size + face_y
            mapped_point = (mapped_point_x, mapped_point_y)
            mapped_points.append(mapped_point)

    rounded_points = []
    for mapped_point in mapped_points:
        rounded_point_x = clean_round(mapped_point[0])
        rounded_point_y = clean_round(mapped_point[1])
        rounded_point = (rounded_point_x, rounded_point_y)
        rounded_points.append(rounded_point)

    return rounded_points


def clean_round(number):
    number = round(number, 2)

    if number == int(number):
        return int(number)

    return number


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
        fill="{color}"/>"""

    return face


def generate_svg(poligons, filename):
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg">
"""

    for poligon in poligons:
        svg += f"   {poligon}\n"

    svg += "</svg>"
    with open(f"{filename}.svg", "w") as file:
        file.write(svg)


def filesize(filename):
    file = open(f"{filename}.svg", "rb")
    file.seek(0, 2)
    size = file.tell()
    file.close()
    return size


def main():
    filename = "menger-sponge"

    up_color = "#ff0000"
    left_color = "#00ff00"
    right_color = "#0000ff"
    colors = [up_color, left_color, right_color]

    iteration = 1
    face_x, face_y = 100, 100
    size = 50
    ratio = [3, 4, 3]

    face_points = generate_face(iteration)
    up_face = draw_face(face_points, face_x, face_y, size, ratio, UP, colors)
    left_face = draw_face(face_points, face_x, face_y, size, ratio, LEFT, colors)
    right_face = draw_face(face_points, face_x, face_y, size, ratio, RIGHT, colors)

    poligons = [up_face, left_face, right_face]
    generate_svg(poligons, filename)

    size = filesize(filename)
    print(f"{filename}.svg has a size of {size} bytes")


if __name__ == "__main__":
    main()
