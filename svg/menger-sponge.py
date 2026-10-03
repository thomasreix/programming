def main():
    filename = "menger-sponge"

    up_color = "#ff0000"
    left_color = "#00ff00"
    right_color = "#0000ff"
    colors = [up_color, left_color, right_color]



    svg = f"""<svg xmlns="http://www.w3.org/2000/svg">
        <polygon points="{points}" fill="lightcoral" stroke="darkred" stroke-width="4" />
    </svg>"""

    with open("square.svg", "w") as file:
        file.write(svg)

print("SVG square successfully generated as 'square.svg'!")


if __name__ == "__main__":
    main()
