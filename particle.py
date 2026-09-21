import sys
import random
import pygame
from math import sqrt


def initialize_particles(number_of_particles, height, width, types):
    particles = []

    if isinstance(types, int):
        number_of_each_particle = number_of_particles // types
        for particle_type in range(types):
            for _ in range(number_of_each_particle):
                x = random.randint(10, width - 10)
                y = random.randint(10, height - 10)
                particles.append([pygame.math.Vector2(x, y), particle_type])
        return particles

    number_of_each_particle = number_of_particles // len(types)
    for i in types:
        for _ in range(number_of_each_particle):
            x = random.randint(10, width - 10)
            y = random.randint(10, height - 10)
            particles.append([pygame.math.Vector2(x, y), i])

    return particles


def update_particles(particles, speed, size, types, width, height):
    new_particles = []
    for main_particle in particles:
        new_velocity = pygame.math.Vector2(0, 0)

        for other_particle in particles:
            if main_particle != other_particle:
                vector = other_particle[0] - main_particle[0]
                distance = vector.length()

                if distance > 0:
                    direction = types[main_particle[1]][0][other_particle[1]]
                    force = (direction / sqrt(distance)) * speed
                    temp_velocity = vector.normalize() * force
                    new_velocity += temp_velocity

        new_position = main_particle[0] + new_velocity

        if new_position.x < size:
            new_position.x = size
        elif new_position.x > width - size:
            new_position.x = width - size

        if new_position.y < size:
            new_position.y = size
        elif new_position.y > height - size:
            new_position.y = height - size

        new_particles.append([new_position, main_particle[1]])

    for _ in range(4):
        for i in range(len(new_particles)):
            for j in range(i + 1, len(new_particles)):
                vector = new_particles[j][0] - new_particles[i][0]
                distance = vector.length()

                if distance == 0:
                    new_particles[j][0].x += random.choice([-1, 1])
                    new_particles[j][0].y += random.choice([-1, 1])
                elif distance < (size * 2):
                    overlap = (size * 2) - distance
                    push = vector.normalize() * (overlap * 0.5)
                    new_particles[i][0] -= push
                    new_particles[j][0] += push

                    for k in [i, j]:
                        if new_particles[k][0].x < size:
                            new_particles[k][0].x = size
                        elif new_particles[k][0].x > width - size:
                            new_particles[k][0].x = width - size

                        if new_particles[k][0].y < size:
                            new_particles[k][0].y = size
                        elif new_particles[k][0].y > height - size:
                            new_particles[k][0].y = height - size

    return new_particles


def main():
    pygame.init()

    width = 960
    height = 540
    screen = pygame.display.set_mode((width, height))

    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    black = (0, 0, 0)

    types = [
        [(1, -1, -1), red],
        [(1, -1, 1), green],
        [(1, -1, 0), blue],
    ]

    particles = initialize_particles(180, height, width, (0, 1))

    speed = 10
    size = 4

    clock = pygame.time.Clock()

    while True:
        clock.tick(60)
        screen.fill(black)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        for position, interaction in particles:
            color = types[interaction][1]
            pygame.draw.circle(
                screen,
                color,
                (int(position.x), int(position.y)),
                size,
            )

        particles = update_particles(particles, speed, size, types, width, height)

        pygame.display.flip()


if __name__ == "__main__":
    main()
