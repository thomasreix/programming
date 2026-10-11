def generate_svg(polygons, filename):
    svg = """<svg xmlns="http://www.w3.org/2000/svg">"""

    for polygon in polygons:
        point_string = ""
        color = polygon[0]
        points = len(polygon) - 1
        for i in range(points):
            x = polygon[i + 1][0]
            y = polygon[i + 1][1]
            point_string += f"{x},{y}"
            if i < points - 1:
                point_string += " "

        svg += f"""\n<polygon points="{point_string}" fill="{color}"/>"""

    svg += "\n</svg>"

    file_size = len(svg.encode("utf-8"))
    print(f"{filename}.svg is {file_size} bytes")

    with open(f"{filename}.svg", "w") as file:
        file.write(svg)
