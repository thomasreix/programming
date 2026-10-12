import sys

import pygame


def main():
    pygame.init()

    width, height = 960, 540
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("bouncing_ball_circle_lifelike")

    white = (255, 255, 255)
    black = (0, 0, 0)

    center = pygame.math.Vector2(width / 2, height / 2)
    position = pygame.math.Vector2(center)
    velocity = pygame.math.Vector2(5.4, 9.6)
    radius = 20

    gravity = pygame.math.Vector2(0, 0.4)
    restitution = 0.99
    circle_radius = 240

    clock = pygame.time.Clock()

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        velocity += gravity
        position += velocity

        offset = position - center
        if offset.length() >= circle_radius - radius:
            normal = offset.normalize()
            velocity = velocity.reflect(normal) * restitution
            position = center + normal * (circle_radius - radius)

        screen.fill(black)
        pygame.draw.circle(screen, white, center, circle_radius, 10)
        pygame.draw.circle(screen, white, position, radius)
        pygame.display.flip()


if __name__ == "__main__":
    main()
