
import pygame
import sys

# Inicialização do Pygame
pygame.init()

# Configurações da tela
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Controle de Quadrado com Joystick")

# Cores
WHITE = (255, 255, 255)
SQUARE_SIZE = 50

# Posição inicial do quadrado
square_x, square_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2

# Configuração do joystick
joysticks = pygame.joystick.get_count()
if joysticks > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

# Loop principal
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Leitura dos valores do joystick
    x_axis = joystick.get_axis(0)
    y_axis = joystick.get_axis(1)

    # Atualização da posição do quadrado
    square_x += int(x_axis * SQUARE_SIZE)
    square_y += int(y_axis * SQUARE_SIZE)

    # Desenho do quadrado
    screen.fill(WHITE)
    pygame.draw.rect(screen, (0, 0, 0), (square_x, square_y, SQUARE_SIZE, SQUARE_SIZE))

    pygame.display.flip()
    pygame.time.Clock().tick(60)


