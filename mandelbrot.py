import pygame


def recursive(z, c, p):
    for i in range(256):
        if z == 0:
            z = c
        else:
            z = z**p + c
        if abs(z) > 2:
            break
    return i


def coloring(i, r, g, b):
    red = i * r % 255
    blue = i * g % 255
    green = i * b % 255
    color = (red, blue, green)
    return color


def main():
    pygame.init()

    width = 960
    height = 540
    screen = pygame.display.set_mode((width, height))

    scale = height / 2
    position = (width / 2, height / 2)
    # position = (width - height / 2, height / 2)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        for x in range(width):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            for y in range(height):
                pixel = complex((x - position[0]) / scale, (position[1] - y) / scale)
                z = 0
                c = complex(0.6, 0.9)
                p = pixel
                # z = complex(0.2, -0.8)
                # z = complex(0.5, 0.2)

                recurtions = recursive(z, c, p)
                color = coloring(recurtions, 9, 16, 25)
                screen.set_at((x, y), color)
            pygame.display.update(x, 0, 1, height)


if __name__ == "__main__":
    main()
