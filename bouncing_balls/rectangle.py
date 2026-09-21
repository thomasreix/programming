import sys

import pygame


def main():
    pygame.init()

    width, height = 960, 540
    pygame.display.set_caption("bouncing_ball_rectangle")
    screen = pygame.display.set_mode((width, height))

    white = (255, 255, 255)
    black = (0, 0, 0)

    position = pygame.math.Vector2(width / 2, height / 2)
    velocity = pygame.math.Vector2(0.9, -1.6)
    radius = 24

    clock = pygame.time.Clock()

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        position += velocity

        if position.x - radius <= 0 or position.x + radius >= width:
            velocity.x *= -1

        if position.y - radius <= 0 or position.y + radius >= height:
            velocity.y *= -1

        screen.fill(black)
        pygame.draw.circle(screen, white, position, radius)
        pygame.display.flip()


if __name__ == "__main__":
    main()
