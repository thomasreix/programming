def render(polygons, filename, stroke):
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
        if stroke:
            point_string = ""
            color = "#000"
            points = len(polygon) - 1
            for i in range(points):
                x = polygon[i + 1][0]
                y = polygon[i + 1][1]
                point_string += f"{x},{y}"
                if i < points - 1:
                    point_string += " "

            svg += f"""\n<polygon points="{point_string}" fill="#0000" stroke="{color}"/>"""

    svg += "\n</svg>"

    file_size = len(svg.encode("utf-8"))
    print(f"{filename}.svg is {file_size} bytes")

    with open(f"tilings/{filename}.svg", "w") as file:
        file.write(svg)


def map(polygons, scale, offset):
    mapped_polygons = []
    for polygon in polygons:
        mapped_polygon = [polygon[0]]
        for vertex in polygon[1:]:
            mapped_vertex = (
                vertex[0] * scale + offset[0],
                vertex[1] * scale + offset[1],
            )
            mapped_polygon.append(mapped_vertex)
        mapped_polygons.append(mapped_polygon)
    return mapped_polygons
