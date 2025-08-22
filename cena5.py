import pygame
import math
import colorsys
import time

# =======================
# Configurações da cena
# =======================
raio_base = 220
raio = raio_base
centro_x = 400
centro_y = 300
angulo_rot = 0
vel_rot = 0.004
psy_mode = False
strobe_mode = False
hue = 0.0
BPM = 130
SUBDIVISAO = 2
strobe_interval = 60.0 / (BPM * SUBDIVISAO)
last_strobe_time = time.time()
strobe_on = False
pulsar_global = False
FONT_SIZE = 40
TEXTO = "EPOD."
base_font = None
start_time = time.time()
num_linhas = 18

# =======================
# Inicialização
# =======================
def init_scene(w, h):
    """Define centro da cena e inicializa fonte."""
    global centro_x, centro_y, base_font
    centro_x = w // 2
    centro_y = h // 2
    if base_font is None:
        if not pygame.font.get_init():
            pygame.font.init()
        base_font = pygame.font.SysFont("Arial Black", FONT_SIZE, bold=True)

# =======================
# Controle de eventos
# =======================
def handle_event(evento, tela=None):
    """Gerencia teclas da Cena 5."""
    global psy_mode, strobe_mode, BPM, raio_base, pulsar_global
    if evento.type == pygame.KEYDOWN:
        if evento.key == pygame.K_z:
            psy_mode = not psy_mode
            print(f"[Cena 5] Psy Mode: {psy_mode}")
        elif evento.key == pygame.K_x:
            strobe_mode = not strobe_mode
            print(f"[Cena 5] Strobe Mode: {strobe_mode}")
        elif evento.key == pygame.K_UP:
            BPM += 1
            update_strobe_interval()
            print(f"[Cena 5] BPM: {BPM}")
        elif evento.key == pygame.K_DOWN:
            BPM = max(1, BPM - 1)
            update_strobe_interval()
            print(f"[Cena 5] BPM: {BPM}")
        elif evento.key == pygame.K_LEFT:
            raio_base = max(50, raio_base - 10)
            print(f"[Cena 5] Raio base: {raio_base}")
        elif evento.key == pygame.K_RIGHT:
            raio_base = min(500, raio_base + 10)
            print(f"[Cena 5] Raio base: {raio_base}")
        elif evento.key == pygame.K_c:
            pulsar_global = not pulsar_global
            print(f"[Cena 5] Pulsar global: {pulsar_global}")

def update_strobe_interval():
    """Atualiza intervalo do strobe baseado no BPM atual."""
    global strobe_interval
    strobe_interval = 60.0 / (BPM * SUBDIVISAO)

# =======================
# Renderização da cena
# =======================
def update_and_draw(tela):
    """Renderiza as letras em padrão circular 3D com efeitos de psy e strobe."""
    global angulo_rot, raio, hue, strobe_on, last_strobe_time, base_font

    # Inicializa fonte se necessário
    if base_font is None:
        init_scene(tela.get_width(), tela.get_height())

    # Fundo strobe
    background_color = (0, 0, 0)
    if strobe_mode:
        now = time.time()
        if now - last_strobe_time >= strobe_interval:
            strobe_on = not strobe_on
            last_strobe_time = now
        background_color = (255, 255, 255) if strobe_on else (232, 104, 0)
    tela.fill(background_color)

    # Rotação global
    angulo_rot += vel_rot

    # Pulsação global do raio
    pulsacao_global = 20 * math.sin(time.time() * 2) if pulsar_global else 0
    raio = raio_base + pulsacao_global

    # Renderização das letras
    letras_renderizadas = []
    for j in range(num_linhas):
        phi = math.pi * (j / (num_linhas - 1) - 0.5)
        r_linha = raio * math.cos(phi)
        y = centro_y + raio * math.sin(phi)
        escala_base = max(0.25, math.cos(phi))
        pulsacao = 0.1 * math.sin(time.time() * 3 + j)
        escala = escala_base + pulsacao
        largura_letra = FONT_SIZE * escala * 1.5
        num_reps = max(6, int((2 * math.pi * r_linha) / largura_letra))

        for i in range(num_reps):
            theta = (i / num_reps) * 2 * math.pi + angulo_rot
            x3d = r_linha * math.cos(theta)
            z3d = r_linha * math.sin(theta)

            if z3d > 0:  # Apenas letras "na frente"
                x = centro_x + x3d
                letra = TEXTO[(i + j) % len(TEXTO)]

                # Cor da letra
                if psy_mode:
                    hue = (hue + 0.004) % 1.0
                    r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb((hue + i * 0.05 + j * 0.05) % 1.0, 1, 1)]
                    cor = (r, g, b)
                elif strobe_mode:
                    cor = (232, 104, 0) if background_color == (255, 255, 255) else (255, 255, 255)
                else:
                    cor = (232, 104, 0)

                # Renderiza a letra com escala
                letra_surface = base_font.render(letra, True, cor)
                letra_surface = pygame.transform.smoothscale(
                    letra_surface,
                    (int(letra_surface.get_width() * escala),
                     int(letra_surface.get_height() * escala))
                )

                # Alpha progressivo (delay de animação)
                rect = letra_surface.get_rect(center=(x, y))
                tempo_passado = time.time() - start_time
                delay = (i * 0.05) + (j * 0.02)
                alpha = 255 if tempo_passado > delay else 0
                if alpha > 0:
                    letra_surface.set_alpha(alpha)
                    letras_renderizadas.append((z3d, letra_surface, rect))

    # Desenha letras ordenadas por profundidade (Z)
    letras_renderizadas.sort(key=lambda item: item[0], reverse=True)
    for _, letra_surface, rect in letras_renderizadas:
        tela.blit(letra_surface, rect)
