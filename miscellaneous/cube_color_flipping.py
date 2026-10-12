def get_empty_cube(size: int) -> list[list[list]]:
    cube = []
    for x in range(size):
        cube_slice = []
        for x in range(size):
            cube_row = []
            for x in range(size):
                cube_row.append(0)
            cube_slice.append(cube_row)
        cube.append(cube_slice)
    return cube


def flip_x(cube: list[list[list]], position: int) -> list[list[list]]:
    fliped_cube = []
    for cube_slice in cube:
        fliped_row = []
        cube_row = cube_slice[position]
        for cube_cube in cube_row:
            cube_cube += 1
            cube_cube %= 2
            fliped_row.append(cube_cube)
        fliped_slice = cube_slice
        fliped_slice[position] = fliped_row
        fliped_cube.append(fliped_slice)
    return fliped_cube


def flip_y(cube: list[list[list]], position) -> list[list[list]]:
    fliped_slice = []
    for cube_row in cube[position]:
        fliped_row = []
        for cube_cube in cube_row:
            cube_cube += 1
            cube_cube %= 2
            fliped_row.append(cube_cube)
        fliped_slice.append(fliped_row)
    fliped_cube = cube
    fliped_cube[position] = fliped_slice
    return fliped_cube


def flip_z(cube: list[list[list]], position) -> list[list[list]]:
    fliped_cube = []
    for cube_slice in cube:
        fliped_slice = []
        for cube_row in cube_slice:
            fliped_row = cube_row
            cube_cube = cube_row[position]
            cube_cube += 1
            cube_cube %= 2
            fliped_row[position] = cube_cube
            fliped_slice.append(fliped_row)
        fliped_cube.append(fliped_slice)
    return fliped_cube


def get_fliped_cube(size: int, x: int, y: int, z: int) -> list[list[list]]:
    cube = get_empty_cube(size)
    for position in range(x):
        cube = flip_x(cube, position)
    for position in range(y):
        cube = flip_y(cube, position)
    for position in range(z):
        cube = flip_z(cube, position)
    return cube


def count_odd_cubes(cube: list[list[list]]) -> int:
    odd_cubes = 0
    for cube_slice in cube:
        for cube_row in cube_slice:
            for cube_cube in cube_row:
                if cube_cube == 1:
                    odd_cubes += 1
    return odd_cubes


def main():
    size = 5

    odd_cubes_amouts = []
    for x in range(size + 1):
        for y in range(size + 1):
            for z in range(size + 1):
                cube = get_fliped_cube(size, x, y, z)
                odd_cubes = count_odd_cubes(cube)

                new = True
                for odd_cubes_amout in odd_cubes_amouts:
                    if odd_cubes == odd_cubes_amout:
                        new = False

                if new:
                    odd_cubes_amouts.append(odd_cubes)

    print(odd_cubes_amouts)
    sum = 0
    for odd_cubes_amout in odd_cubes_amouts:
        sum += odd_cubes_amout
    print(sum)
    total = len(odd_cubes_amouts)
    print(total)


if __name__ == "__main__":
    main()
