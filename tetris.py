import sys

import pygame
import random


def main():
    pygame.init()

    width = 540
    screen = pygame.display.set_mode((width, width))

    clock = pygame.time.Clock()
    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()


if __name__ == "__main__":
    main()
