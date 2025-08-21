import pygame
import sys
import colorsys
import random

# Inicializa o pygame
pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Telão DJ - DOPE")

# Configurações da fonte
FONT_SIZE = 100
font = pygame.font.SysFont("Arial Black", FONT_SIZE, bold=True)

# Texto
text = " DOPE "

# Divide a tela em 5 faixas
num_faixas = 5
faixa_altura = HEIGHT // num_faixas

# Velocidade do letreiro em pixels/frame
speed = 3

# Para cada faixa, guardamos o deslocamento inicial
offsets = [0 for _ in range(num_faixas)]

# Texto base em branco
text_surface_base = font.render(text, True, (255, 255, 255))
text_width = text_surface_base.get_width()
text_height = text_surface_base.get_height()

# Controle de psicodelia
psy_mode = False
hue = 0  # matiz inicial (0-1)

# Loop principal
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
                psy_mode = not psy_mode  # alterna o modo psicodélico

    screen.fill((0, 0, 0))  # fundo preto

    for i in range(num_faixas):
        y = i * faixa_altura + (faixa_altura - text_height) // 2

        # Direção alternada: par → direita→esquerda, ímpar → esquerda→direita
        direction = -1 if i % 2 == 0 else 1
        offsets[i] += direction * speed
        offsets[i] %= text_width  

        # Escolhe a cor
        if psy_mode:
            # Gera cor psicodélica usando HSL → RGB
            hue = (hue + 0.002) % 1.0
            r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb((hue + i*0.15) % 1.0, 1, 1)]
            text_surface = font.render(text, True, (r, g, b))
        else:
            text_surface = text_surface_base

        # Desenha repetidamente para encher a faixa
        for x in (offsets[i], offsets[i] - text_width):
            pos_x = x
            while pos_x < WIDTH:
                screen.blit(text_surface, (pos_x, y))
                pos_x += text_width

    pygame.display.flip()
    clock.tick(60)  # 60 FPS
