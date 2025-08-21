import pygame
import colorsys
import time
from utils import LARGURA, ALTURA

# Configurações da fonte e texto
FONT_SIZE = 100
font = pygame.font.SysFont("Arial Black", FONT_SIZE, bold=True)
text = " DOPE "

# Divide a tela em 5 faixas
num_faixas = 5
faixa_altura = ALTURA // num_faixas

# Velocidade do letreiro
speed = 3

# Offsets para cada faixa
offsets = [0 for _ in range(num_faixas)]

# Texto base
text_surface_base = font.render(text, True, (255, 255, 255))
text_width = text_surface_base.get_width()
text_height = text_surface_base.get_height()

# --- Configuração inicial de BPM e subdivisão ---
BPM = 128          # valor inicial
subdivisao = 2     # 1=1 piscada/batida, 2=2 piscadas/batida, 4=4 piscadas/batida
strobe_interval = 60.0 / (BPM * subdivisao)

# Modos
psy_mode = False
strobe_mode = False
hue = 0

# Controle strobe
last_strobe_time = time.time()
strobe_on = False

def update_strobe_interval():
    """Atualiza o intervalo do strobe baseado no BPM e subdivisão"""
    global strobe_interval
    strobe_interval = 60.0 / (BPM * subdivisao)

def handle_event(evento, tela=None):
    global psy_mode, strobe_mode, BPM

    if evento.type == pygame.KEYDOWN:
        if evento.key == pygame.K_z:
            psy_mode = not psy_mode
            print(f"[Cena 4] Psicodelia: {psy_mode}")

        elif evento.key == pygame.K_x:
            strobe_mode = not strobe_mode
            print(f"[Cena 4] Strobe: {strobe_mode}")

        elif evento.key == pygame.K_UP:
            BPM += 1
            update_strobe_interval()
            print(f"[Cena 4] BPM aumentado para {BPM}")

        elif evento.key == pygame.K_DOWN:
            if BPM > 1:  # evita BPM zero ou negativo
                BPM -= 1
                update_strobe_interval()
                print(f"[Cena 4] BPM diminuído para {BPM}")

def cena4(tela):
    global hue, last_strobe_time, strobe_on

    largura, altura = tela.get_size()
    faixa_altura = altura // num_faixas

    # Fundo padrão
    background_color = (0, 0, 0)

    # Strobe
    if strobe_mode:
        now = time.time()
        if now - last_strobe_time >= strobe_interval:
            strobe_on = not strobe_on
            last_strobe_time = now
        background_color = (255, 255, 255) if strobe_on else (0, 0, 0)

    tela.fill(background_color)

    for i in range(num_faixas):
        y = i * faixa_altura + (faixa_altura - text_height) // 2

        # Direção alternada
        direction = -1 if i % 2 == 0 else 1
        offsets[i] += direction * speed
        offsets[i] %= text_width

        # Cor do texto
        if psy_mode:
            hue = (hue + 0.002) % 1.0
            r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb((hue + i*0.15) % 1.0, 1, 1)]
            text_surface = font.render(text, True, (r, g, b))
        else:
            if strobe_mode:
                text_surface = font.render(
                    text,
                    True,
                    (0, 0, 0) if background_color == (255, 255, 255) else (255, 255, 255)
                )
            else:
                text_surface = text_surface_base

        # Preenche a faixa
        for x in (offsets[i], offsets[i] - text_width):
            pos_x = x
            while pos_x < largura:
                tela.blit(text_surface, (pos_x, y))
                pos_x += text_width
