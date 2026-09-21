import sys

import pygame
from pygame.math import Vector2
from pygame.time import Clock


def new_position_velocity(
    pos: Vector2, vel: Vector2, radius: int, width: int, height: int
) -> tuple[Vector2, Vector2]:
    new_pos = pos + vel
    new_vel = vel

    if new_pos.x < radius:
        new_pos.x = 2 * radius - new_pos.x
        new_vel.x *= -1

    if new_pos.x + radius >= width:
        pos.x = 2 * width - new_pos.x
        new_vel.x *= -1

    if new_pos.y < radius:
        new_pos.y = 2 * radius - new_pos.y
        vel.y *= -1

    if new_pos.y + radius >= height:
        new_pos.y = 2 * (height - radius) - new_pos.y
        vel.y *= -1

    wall_y = 270
    if new_pos.x - radius > 240 and new_pos.x + radius < 720:
        if pos.y + radius < wall_y and new_pos.y + radius >= wall_y:
            new_pos.y = wall_y - radius
            new_vel.y *= -1
        if pos.y - radius > wall_y and new_pos.y - radius <= wall_y:
            new_pos.y = wall_y + radius
            new_vel.y *= -1

    return new_pos, new_vel


def main():
    pygame.init()

    width, height = 960, 540
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Bouncing Ball with a wall")

    white = (255, 255, 255)
    black = (0, 0, 0)

    pos = Vector2(width / 2, height / 3)

    vel = Vector2(0.9, -1.6)
    radius = 12

    x1 = 270
    y = 270
    x2 = width - x1

    clock = Clock()
    while True:
        clock.tick(120)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pos, vel = new_position_velocity(pos, vel, radius, width, height)

        screen.fill(black)
        pygame.draw.line(screen, white, (x1, y), (x2, y), 3)
        pygame.draw.circle(screen, white, pos, radius)
        pygame.display.flip()


if __name__ == "__main__":
    main()
