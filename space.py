import math
import pygame


pygame.init()

pygame.display.set_caption("Platformer")

WIDTH, HEIGHT = 1000, 800

window = pygame.display.set_mode((WIDTH, HEIGHT))

sprite_sheet = pygame.image.load("ship01.png").convert_alpha()

rectShip01 = pygame.Rect(96, 128, 10, 10)

posXShip01 = 30
posYShip01 = 50



run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
                break


    pygame.display.update()
    