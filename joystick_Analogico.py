
import pygame
import sys

# Inicialização do pygame
pygame.init()
 
# Configuração da tela
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Controle de Ponto com Joystick")
 
# Configuração do joystick
joystick = None
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
 
# Cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
 
# Posição inicial do ponto
x, y = width // 2, height // 2
 
# Velocidade inicial do ponto
speed = 1.2
 
# Loop principal do jogo
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
 
    # Limpeza da tela
    screen.fill(BLACK)
 
    # Atualização da posição do ponto
    if joystick:
        # Obtendo os valores do joystick
        joystick_x = joystick.get_axis(0)
        joystick_y = joystick.get_axis(1)

        print("joystick_x = ",joystick_x)
        print("joystick_y = ",joystick_y)
 
        # Atualizando a posição do ponto com base nos valores do joystick
        x += int(joystick_x * speed)
        y += int(joystick_y * speed)
 
    # Desenho do ponto na tela
    pygame.draw.circle(screen, WHITE, (x, y), 10)
 
    # Atualização da tela
    pygame.display.flip()