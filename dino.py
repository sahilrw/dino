import sys
import pygame

WIDTH = 623
HEIGHT = 150

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dino Game")


def main():
    while True:
        for event in pygame.event.get():
            # end the game on clicking quit button
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            pygame.display.update()


main()
