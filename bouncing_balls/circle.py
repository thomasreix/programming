import sys

import pygame


def main():
    pygame.init()

    width = 960
    height = 540
    pygame.display.set_caption("bouncing_ball_circle")
    screen = pygame.display.set_mode((width, height))

    white = (255, 255, 255)
    black = (0, 0, 0)

    center = pygame.math.Vector2(width / 2, height / 2)
    position = pygame.math.Vector2(center)
    velocity = pygame.math.Vector2(5.4, 9.6)
    radius = 20

    clock = pygame.time.Clock()

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        position += velocity

        offset = position - center
        if offset.length() >= 240 - radius:
            theta = offset.normalize()
            velocity = velocity.reflect(theta)

        screen.fill(black)
        pygame.draw.circle(screen, white, (width / 2, height / 2), 240, 10)
        pygame.draw.circle(screen, white, position, radius)
        pygame.display.flip()


if __name__ == "__main__":
    main()
