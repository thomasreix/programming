cube_vertices = [
    [0, 0, 0],
    [1, 0, 0],
    [1, 1, 0],
    [0, 1, 0],
    [0, 0, 1],
    [1, 0, 1],
    [1, 1, 1],
    [0, 1, 1],
]

cube_faces = [
    [0, 2, 1],
    [0, 3, 2],
    [4, 5, 6],
    [4, 6, 7],
    [0, 1, 5],
    [0, 5, 4],
    [2, 3, 7],
    [2, 7, 6],
    [1, 2, 6],
    [1, 6, 5],
    [3, 0, 4],
    [3, 4, 7],
]


def next_iteration(original_cube):
    cubes = []
    for x in range(3):
        for y in range(3):
            for z in range(3):
                if not (
                    (x == 1 and y == 1) or (y == 1 and z == 1) or (z == 1 and x == 1)
                ):
                    cube = (
                        x + original_cube[0] * 3,
                        y + original_cube[1] * 3,
                        z + original_cube[2] * 3,
                    )
                    cubes.append(cube)
    return cubes


def main():
    iteration = 1

    menger_cubes = [(0, 0, 0)]

    for _ in range(iteration):
        new_cubes = []
        for cube in menger_cubes:
            generated_cubes = next_iteration(cube)
            new_cubes.extend(generated_cubes)
        menger_cubes = new_cubes

    filename = f"menger_sponge_{iteration}"
    with open(f"{filename}.stl", "w") as output_file:
        output_file.write("solid menger_sponge\n")

        for cube in menger_cubes:
            cube_x, cube_y, cube_z = cube
            for face in cube_faces:
                output_file.write("  facet normal 0 0 0\n")
                output_file.write("    outer loop\n")
                for vertex_index in face:
                    cube_vertex = cube_vertices[vertex_index]

                    vertex_x = cube_x + cube_vertex[0]
                    vertex_y = cube_y + cube_vertex[1]
                    vertex_z = cube_z + cube_vertex[2]

                    output_file.write(
                        f"      vertex {vertex_x:.6f} {vertex_y:.6f} {vertex_z:.6f}\n"
                    )
                output_file.write("    endloop\n")
                output_file.write("  endfacet\n")

        output_file.write("endsolid menger_sponge\n")


if __name__ == "__main__":
    main()
