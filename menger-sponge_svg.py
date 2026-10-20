from svg_utils import generate_svg


def compute_sponge(iteration: int) -> list[tuple[int, int, int]]:
    voxels = [(0, 0, 0)]
    for i in range(iteration):
        new_voxels = []
        for voxel in voxels:
            for x in range(3):
                for y in range(3):
                    for z in range(3):
                        if not (
                            (x == 1 and y == 1)
                            or (y == 1 and z == 1)
                            or (z == 1 and x == 1)
                        ):
                            new_voxel_x = voxel[0] * 3 + x
                            new_voxel_y = voxel[1] * 3 + y
                            new_voxel_z = voxel[2] * 3 + z
                            new_voxel = (new_voxel_x, new_voxel_y, new_voxel_z)
                            new_voxels.append(new_voxel)
        voxels = new_voxels

    return voxels


def order_voxels(
    voxels: list[tuple[int, int, int]], iteration: int
) -> list[tuple[int, int, int]]:
    diagonal = 3 ** (iteration + 1)
    ordered_voxels = []
    for i in range(diagonal):
        for voxel in voxels:
            x, y, z = voxel
            if (x + y + z) == i:
                ordered_voxels.append(voxel)

    return ordered_voxels


def project_voxels(
    voxels: list[tuple[int, int, int]],
    iteration: int,
    size: int,
    position: tuple[int, int],
    proportions: tuple[int, int, int],
    colors: list[str],
) -> list[list[str, tuple]]:
    a, b, c = proportions
    polygons = []
    for voxel in voxels:
        x = voxel[0] * c - voxel[2] * a
        y = voxel[0] + voxel[2] - voxel[1] * b
        points = [
            (x + c, y),
            (x, y + 1),
            (x + c + a, y + 1),
            (x + a, y + 2),
            (x, y + b + 1),
            (x + a + c, y + b + 1),
            (x + a, y + b + 2),
        ]

        scaled_points = []
        for point in points:
            scaled_point_x = point[0] * size + position[0]
            scaled_point_y = point[1] * size + position[1]
            scaled_point = (scaled_point_x, scaled_point_y)
            scaled_points.append(scaled_point)

        face_up = [
            colors[0],
            scaled_points[0],
            scaled_points[1],
            scaled_points[3],
            scaled_points[2],
        ]
        polygons.append(face_up)
        face_left = [
            colors[1],
            scaled_points[1],
            scaled_points[4],
            scaled_points[6],
            scaled_points[3],
        ]
        polygons.append(face_left)
        face_right = [
            colors[2],
            scaled_points[3],
            scaled_points[6],
            scaled_points[5],
            scaled_points[2],
        ]
        polygons.append(face_right)

    return polygons


def main():
    filename = "menger-sponge"

    up_color = "#f00"
    left_color = "#0f0"
    right_color = "#00f"
    colors = [up_color, left_color, right_color]

    iteration = 1
    size = 10
    position = (400, 400)
    proportions = (3, 4, 3)

    menger_voxels = compute_sponge(iteration)
    ordered_voxels = order_voxels(menger_voxels, iteration)
    polygons = project_voxels(
        ordered_voxels, iteration, size, position, proportions, colors
    )

    generate_svg(polygons, filename)


if __name__ == "__main__":
    main()
