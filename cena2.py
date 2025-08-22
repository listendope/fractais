import pygame
import random
import time
import math
from utils import hsv_para_rgb, aplicar_rgb_split, aplicar_glitch_slices, agendar_proximo_glitch

# -----------------------------
# Parâmetros gerais da cena 2
# -----------------------------
GLITCH_INTENSIDADE = 0.80
RGB_SPLIT_PX = 3
GLITCH_INTERVALO_MIN = 0.4
GLITCH_INTERVALO_MAX = 0.6

PSY_CIRCULO_ESPACO = 28
PSY_ARCO_RAIOS = 18
PSY_RAIOS_QTD = 24

# Limites para modulação
GLITCH_INTERVALO_MIN_LIM = 0.01
GLITCH_INTERVALO_MAX_LIM = 2.00
PSY_RAIOS_MIN = 2
PSY_RAIOS_MAX = 200
PSY_CIRCULO_ESPACO_MIN = 2
PSY_CIRCULO_ESPACO_MAX = 80

# Passos automáticos para auto-modulação
AUTO_MOD_INTERVALO = 0.05
AUTO_RAIOS_STEP = 2
AUTO_ESPACO_STEP = 1

# -----------------------------
# Estado global da Cena 2
# -----------------------------
tempo_base_cena2 = time.time()
proximo_glitch = time.time() + random.uniform(GLITCH_INTERVALO_MIN, GLITCH_INTERVALO_MAX)
auto_psy_modulacao = False
ultimo_auto_mod_tempo = time.time()
raios_direcao = 1
espaco_direcao = 1
glitch_ativo = False


# -----------------------------
# Função de tratamento de eventos
# -----------------------------
def handle_event(evento):
    """
    Processa os eventos da cena 2:
    - R: alterna auto-modulação de raios/espacamento
    - W: alterna efeito glitch
    - ↑/↓: ajusta intervalo do glitch
    - ←/→: ajusta quantidade de raios
    - A/D: ajusta espaçamento dos círculos
    """
    global auto_psy_modulacao, GLITCH_INTERVALO_MIN, GLITCH_INTERVALO_MAX
    global PSY_RAIOS_QTD, PSY_CIRCULO_ESPACO, proximo_glitch
    global glitch_ativo

    if evento.type != pygame.KEYDOWN:
        return

    # Auto-modulação
    if evento.key == pygame.K_r:
        auto_psy_modulacao = not auto_psy_modulacao
        estado = "ATIVADA" if auto_psy_modulacao else "DESATIVADA"
        print(f"[Cena 2] Auto-modulação {estado} (Raios e Espaçamento).")
    
    # Toggle glitch
    elif evento.key == pygame.K_w:
        glitch_ativo = not glitch_ativo
        estado = "ATIVADO" if glitch_ativo else "DESATIVADO"
        print(f"[Cena 2] Glitch {estado}.")

    # Ajuste intervalo glitch
    elif evento.key == pygame.K_UP:
        GLITCH_INTERVALO_MIN = min(GLITCH_INTERVALO_MAX_LIM, GLITCH_INTERVALO_MIN + 0.01)
        GLITCH_INTERVALO_MAX = min(GLITCH_INTERVALO_MAX_LIM, GLITCH_INTERVALO_MAX + 0.02)
        GLITCH_INTERVALO_MIN = min(GLITCH_INTERVALO_MIN, GLITCH_INTERVALO_MAX - 0.005)
        proximo_glitch = agendar_proximo_glitch(
            GLITCH_INTENSIDADE, GLITCH_INTERVALO_MIN, GLITCH_INTERVALO_MAX, GLITCH_INTERVALO_MIN_LIM
        )
        print(f"[Cena 2] Intervalo glitch AUMENTADO: {GLITCH_INTERVALO_MIN:.2f} - {GLITCH_INTERVALO_MAX:.2f}")

    elif evento.key == pygame.K_DOWN:
        GLITCH_INTERVALO_MIN = max(GLITCH_INTERVALO_MIN_LIM, GLITCH_INTERVALO_MIN - 0.01)
        GLITCH_INTERVALO_MAX = max(max(GLITCH_INTERVALO_MIN + 0.01, 0.05), GLITCH_INTERVALO_MAX - 0.02)
        proximo_glitch = agendar_proximo_glitch(
            GLITCH_INTENSIDADE, GLITCH_INTERVALO_MIN, GLITCH_INTERVALO_MAX, GLITCH_INTERVALO_MIN_LIM
        )
        print(f"[Cena 2] Intervalo glitch REDUZIDO: {GLITCH_INTERVALO_MIN:.2f} - {GLITCH_INTERVALO_MAX:.2f}")

    # Ajuste quantidade de raios
    elif evento.key == pygame.K_RIGHT:
        PSY_RAIOS_QTD = min(PSY_RAIOS_MAX, PSY_RAIOS_QTD + 2)
        print(f"[Cena 2] Raios: {PSY_RAIOS_QTD}")

    elif evento.key == pygame.K_LEFT:
        PSY_RAIOS_QTD = max(PSY_RAIOS_MIN, PSY_RAIOS_QTD - 2)
        print(f"[Cena 2] Raios: {PSY_RAIOS_QTD}")

    # Ajuste espaçamento dos círculos
    elif evento.key == pygame.K_d:
        PSY_CIRCULO_ESPACO = min(PSY_CIRCULO_ESPACO + 2, PSY_CIRCULO_ESPACO_MAX)
        print(f"[Cena 2] Espaçamento círculos: {PSY_CIRCULO_ESPACO}")

    elif evento.key == pygame.K_a:
        PSY_CIRCULO_ESPACO = max(PSY_CIRCULO_ESPACO - 2, PSY_CIRCULO_ESPACO_MIN)
        print(f"[Cena 2] Espaçamento círculos: {PSY_CIRCULO_ESPACO}")


# -----------------------------
# Função de construção da superfície psicodélica
# -----------------------------
def construir_psicodelia_surface(w, h, t):
    """
    Cria superfície com anéis concêntricos e raios girando
    com variação de cores HSV.
    """
    surf = pygame.Surface((w, h), pygame.SRCALPHA).convert_alpha()
    cx, cy = w // 2, h // 2

    # Aplicar rastro (fade)
    fade = pygame.Surface((w, h), pygame.SRCALPHA)
    fade.fill((0, 0, 0, 60))
    surf.blit(fade, (0, 0))

    # Limitar espaçamento
    espacamento = max(PSY_CIRCULO_ESPACO_MIN, min(PSY_CIRCULO_ESPACO, PSY_CIRCULO_ESPACO_MAX))

    # Desenhar anéis concêntricos
    max_r = int(math.hypot(w, h) / 2) + 40
    base_h = (t * 0.12) % 1.0
    for r in range(espacamento, max_r, espacamento):
        hue = (base_h + r * 0.004) % 1.0
        cor = hsv_para_rgb(hue, 1.0, 1.0)
        pygame.draw.circle(surf, (*cor, 130), (cx, cy), r, PSY_ARCO_RAIOS)

    # Desenhar raios
    ang_base = t * 60  # graus por segundo
    raio_max = max(w, h)
    qnt = max(PSY_RAIOS_MIN, min(PSY_RAIOS_QTD, PSY_RAIOS_MAX))
    for i in range(qnt):
        frac = i / max(1, qnt)
        ang = math.radians(ang_base + frac * 360.0)
        x2 = int(cx + math.cos(ang) * raio_max)
        y2 = int(cy + math.sin(ang) * raio_max)
        hue = (base_h + frac) % 1.0
        cor = hsv_para_rgb(hue, 1.0, 1.0)
        pygame.draw.line(surf, (*cor, 110), (cx, cy), (x2, y2), 3)

    return surf


# -----------------------------
# Render principal da cena 2
# -----------------------------
def cena2(tela):
    """
    Renderiza a cena 2:
    - Base psicodélica
    - Split RGB
    - Glitch em fatias
    - Ruído aleatório
    - Auto-modulação (R)
    """
    global proximo_glitch, ultimo_auto_mod_tempo, PSY_RAIOS_QTD, PSY_CIRCULO_ESPACO
    global raios_direcao, espaco_direcao

    w, h = tela.get_size()
    t = time.time() - tempo_base_cena2

    # --- Auto-modulação ---
    agora = time.time()
    if auto_psy_modulacao and (agora - ultimo_auto_mod_tempo) >= AUTO_MOD_INTERVALO:
        # Modulação de raios
        PSY_RAIOS_QTD += AUTO_RAIOS_STEP * raios_direcao
        if PSY_RAIOS_QTD >= PSY_RAIOS_MAX:
            PSY_RAIOS_QTD = PSY_RAIOS_MAX
            raios_direcao = -1
        elif PSY_RAIOS_QTD <= PSY_RAIOS_MIN:
            PSY_RAIOS_QTD = PSY_RAIOS_MIN
            raios_direcao = 1

        # Modulação do espaçamento dos círculos
        PSY_CIRCULO_ESPACO += AUTO_ESPACO_STEP * espaco_direcao
        if PSY_CIRCULO_ESPACO >= PSY_CIRCULO_ESPACO_MAX:
            PSY_CIRCULO_ESPACO = PSY_CIRCULO_ESPACO_MAX
            espaco_direcao = -1
        elif PSY_CIRCULO_ESPACO <= PSY_CIRCULO_ESPACO_MIN:
            PSY_CIRCULO_ESPACO = PSY_CIRCULO_ESPACO_MIN
            espaco_direcao = 1

        ultimo_auto_mod_tempo = agora

    # --- Construção da base psicodélica ---
    base = construir_psicodelia_surface(w, h, t)

    # --- Aplicar RGB split ---
    split_px = max(1, int(RGB_SPLIT_PX * (0.6 + 0.8 * GLITCH_INTENSIDADE)))
    out = aplicar_rgb_split(base, split_px)

    # --- Aplicar glitch em fatias ---
    now = time.time()
    if glitch_ativo and now >= proximo_glitch:
        out = aplicar_glitch_slices(out, GLITCH_INTENSIDADE)
        proximo_glitch = agendar_proximo_glitch(
            GLITCH_INTENSIDADE, GLITCH_INTERVALO_MIN, GLITCH_INTERVALO_MAX, GLITCH_INTERVALO_MIN_LIM
        )

    # --- Adicionar ruído aleatório ---
    ruido_qtd = int(20 * GLITCH_INTENSIDADE)
    for _ in range(ruido_qtd):
        if random.random() < 0.15 + 0.25 * GLITCH_INTENSIDADE:
            rw = random.randint(4, 18)
            rh = random.randint(2, 12)
            rx = random.randint(0, w - rw)
            ry = random.randint(0, h - rh)
            cor = (
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(30, 90),
            )
            pygame.draw.rect(out, cor, (rx, ry, rw, rh))

    # Render final na tela
    tela.fill((0, 0, 0))
    tela.blit(out, (0, 0))
