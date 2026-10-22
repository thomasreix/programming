from svg_utils import render


def main():
    filename = "polygons"
    polygons = [
        ["#f00", (50, 50), (50, 150), (100, 150), (100, 50)],
        ["#0ff", (30, 30), (30, 180), (130, 180), (130, 30)],
    ]

    render(polygons, filename)


if __name__ == "__main__":
    main()
