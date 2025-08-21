import pygame
import sys
import random
import math
import time
import colorsys

# ---------------- CONFIGURAÇÕES ----------------
LARGURA, ALTURA = 960, 600
FPS = 240
CORES = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (128, 0, 128)]
VELOCIDADE_ZOOM_INICIAL = 0.2

# Cena 1 - modo aleatório
VELOCIDADE_TROCA_COR = 0.2  # segundos
INTERVALO_GERACAO_OBJETOS = 0.5  # segundos

# Cena 2 - parâmetros de glitch/psicodelia (ajustáveis em tempo real)
GLITCH_INTENSIDADE = 0.80     # 0.0 a 1.0 (quanto maior, mais agressivo)
RGB_SPLIT_PX = 3              # deslocamento base em pixels para separação RGB
GLITCH_INTERVALO_MIN = 0.4   # segundos (ajustado nas setas ↑/↓)
GLITCH_INTERVALO_MAX = 0.6   # segundos (ajustado nas setas ↑/↓)
PSY_CIRCULO_ESPACO = 28       # espaçamento entre anéis concêntricos (ajustado automaticamente com 'R')
PSY_ARCO_RAIOS = 18           # espessura do “traço” dos anéis psicodélicos
PSY_RAIOS_QTD = 24            # quantidade de “raios” (linhas girando) (ajustado nas setas ←/→ e auto com 'R')

# Limites para segurança nos ajustes em tempo real
GLITCH_INTERVALO_MIN_LIM = 0.01
GLITCH_INTERVALO_MAX_LIM = 2.00
PSY_RAIOS_MIN = 2
PSY_RAIOS_MAX = 200
PSY_CIRCULO_ESPACO_MIN = 6
PSY_CIRCULO_ESPACO_MAX = 80

# Auto-modulação (Cena 2, tecla R)
AUTO_MOD_INTERVALO = 0.05  # segundos entre passos de modulação
AUTO_RAIOS_STEP = 2         # variação por passo para PSY_RAIOS_QTD
AUTO_ESPACO_STEP = 1        # variação por passo para PSY_CIRCULO_ESPACO

# ---------------- INICIALIZAÇÃO ----------------
pygame.init()
tela = pygame.display.set_mode((LARGURA, ALTURA), pygame.RESIZABLE)
pygame.display.set_caption("Controle de Cor com Cenas")
clock = pygame.time.Clock()

# ---------------- ESTADO GLOBAL ----------------
cena_atual = 1  # Começa na cena 1

# Cena 1
indice_cor = 0
velocidade_zoom = VELOCIDADE_ZOOM_INICIAL
centro = [LARGURA // 2, ALTURA // 2]
angulo_rotacao = 0
velocidade_rotacao = 0
modo_aleatorio = False
ultimo_tempo_cor = time.time()
ultimo_tempo_objeto = time.time()
circulos, quadrados, triangulos = [], [], []

# Cena 2
tempo_base_cena2 = time.time()  # base temporal para animações de cor/rotação
proximo_glitch = time.time() + random.uniform(GLITCH_INTERVALO_MIN, GLITCH_INTERVALO_MAX)
auto_psy_modulacao = False
ultimo_auto_mod_tempo = time.time()
raios_direcao = 1
espaco_direcao = 1
# ---------------- FUNÇÕES AUXILIARES ----------------
def rotacionar_ponto(x, y, cx, cy, angulo):
    rad = math.radians(angulo)
    cos_a, sin_a = math.cos(rad), math.sin(rad)
    dx, dy = x - cx, y - cy
    return (dx * cos_a - dy * sin_a + cx, dx * sin_a + dy * cos_a + cy)

def hsv_para_rgb(h, s, v):
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return (int(r * 255), int(g * 255), int(b * 255))

def desenhar_formas():
    # Círculos
    for c in circulos:
        pygame.draw.circle(tela, (255, 255, 255), c['pos'], int(c['raio']), 2)
        c['raio'] += velocidade_zoom

    # Quadrados
    for q in quadrados:
        lado = int(q['lado'])
        x, y = q['pos']
        pontos = [(x - lado//2, y - lado//2), (x + lado//2, y - lado//2),
                  (x + lado//2, y + lado//2), (x - lado//2, y + lado//2)]
        pontos_rot = [rotacionar_ponto(px, py, x, y, angulo_rotacao) for px, py in pontos]
        pygame.draw.polygon(tela, (255, 255, 255), pontos_rot, 2)
        q['lado'] += velocidade_zoom

    # Triângulos
    for t in triangulos:
        tam = int(t['tamanho'])
        x, y = t['pos']
        pontos = [(x, y - tam//2), (x - tam//2, y + tam//2), (x + tam//2, y + tam//2)]
        pontos_rot = [rotacionar_ponto(px, py, x, y, angulo_rotacao) for px, py in pontos]
        pygame.draw.polygon(tela, (255, 255, 255), pontos_rot, 2)
        t['tamanho'] += velocidade_zoom

def gerar_objeto_aleatorio():
    tipo = random.choice(['c', 'q', 't'])
    pos = (random.randint(0, LARGURA), random.randint(0, ALTURA))
    if tipo == 'c':
        circulos.append({'raio': 1, 'pos': pos})
    elif tipo == 'q':
        quadrados.append({'lado': 1, 'pos': pos})
    elif tipo == 't':
        triangulos.append({'tamanho': 1, 'pos': pos})

def agendar_proximo_glitch(agora=None):
    """Agenda o próximo glitch com base nos intervalos atuais e intensidade."""
    global proximo_glitch
    if agora is None:
        agora = time.time()
    # Mais intensidade -> glitches mais frequentes
    fator = (0.5 + GLITCH_INTENSIDADE)
    intervalo = random.uniform(GLITCH_INTERVALO_MIN, GLITCH_INTERVALO_MAX) / fator
    proximo_glitch = agora + max(GLITCH_INTERVALO_MIN_LIM, intervalo)


# ---------------- EVENTOS ----------------
def processar_eventos():
    global indice_cor, velocidade_zoom, centro, velocidade_rotacao, angulo_rotacao
    global modo_aleatorio, cena_atual, LARGURA, ALTURA
    global GLITCH_INTERVALO_MIN, GLITCH_INTERVALO_MAX, PSY_RAIOS_QTD, proximo_glitch
    global auto_psy_modulacao, PSY_CIRCULO_ESPACO

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            return False

        elif evento.type == pygame.VIDEORESIZE:
            # Ajusta dimensões ao redimensionar a janela
            LARGURA, ALTURA = evento.w, evento.h
            pygame.display.set_mode((LARGURA, ALTURA), pygame.RESIZABLE)

        elif evento.type == pygame.KEYDOWN:
            # Troca de cenas
            if evento.key == pygame.K_1:
                cena_atual = 1
            elif evento.key == pygame.K_2:
                cena_atual = 2
            elif evento.key == pygame.K_3:
                cena_atual = 3

            # Controles da CENA 1
            if cena_atual == 1:
                if evento.key == pygame.K_RIGHT:
                    indice_cor = (indice_cor + 1) % len(CORES)
                elif evento.key == pygame.K_LEFT:
                    indice_cor = (indice_cor - 1) % len(CORES)
                elif evento.key == pygame.K_UP:
                    velocidade_zoom += 0.01
                elif evento.key == pygame.K_DOWN:
                    velocidade_zoom -= 0.01
                elif evento.key == pygame.K_c:
                    circulos.append({'raio': 1, 'pos': tuple(centro)})
                elif evento.key == pygame.K_q:
                    quadrados.append({'lado': 1, 'pos': tuple(centro)})
                elif evento.key == pygame.K_t:
                    triangulos.append({'tamanho': 1, 'pos': tuple(centro)})
                elif evento.key == pygame.K_SPACE:
                    centro = [random.randint(0, LARGURA), random.randint(0, ALTURA)]
                elif evento.key == pygame.K_6:  # anti-horário
                    velocidade_rotacao = velocidade_zoom
                elif evento.key == pygame.K_4:  # horário
                    velocidade_rotacao = -velocidade_zoom
                elif evento.key == pygame.K_5:  # reset
                    velocidade_rotacao = 0
                    angulo_rotacao = 0
                elif evento.key == pygame.K_r:  # modo aleatório
                    modo_aleatorio = not modo_aleatorio

            # Controles da CENA 2
            elif cena_atual == 2:
                # Toggle auto modulação (R)
                if evento.key == pygame.K_r:
                    auto_psy_modulacao = not auto_psy_modulacao
                    estado = "ATIVADA" if auto_psy_modulacao else "DESATIVADA"
                    print(f"[Cena 2] Auto-modulação {estado} (Raios e Espaçamento).")

                # ↑ / ↓ ajustam o intervalo do glitch
                elif evento.key == pygame.K_UP:
                    GLITCH_INTERVALO_MIN = min(GLITCH_INTERVALO_MAX_LIM, GLITCH_INTERVALO_MIN + 0.01)
                    GLITCH_INTERVALO_MAX = min(GLITCH_INTERVALO_MAX_LIM, GLITCH_INTERVALO_MAX + 0.02)
                    # Garante relação min <= max
                    GLITCH_INTERVALO_MIN = min(GLITCH_INTERVALO_MIN, GLITCH_INTERVALO_MAX - 0.005)
                    agendar_proximo_glitch()
                    print(f"[Cena 2] Intervalo glitch AUMENTADO: {GLITCH_INTERVALO_MIN:.2f} - {GLITCH_INTERVALO_MAX:.2f}")

                elif evento.key == pygame.K_DOWN:
                    GLITCH_INTERVALO_MIN = max(GLITCH_INTERVALO_MIN_LIM, GLITCH_INTERVALO_MIN - 0.01)
                    GLITCH_INTERVALO_MAX = max(max(GLITCH_INTERVALO_MIN + 0.01, 0.05), GLITCH_INTERVALO_MAX - 0.02)
                    agendar_proximo_glitch()
                    print(f"[Cena 2] Intervalo glitch REDUZIDO: {GLITCH_INTERVALO_MIN:.2f} - {GLITCH_INTERVALO_MAX:.2f}")

                # ← / → ajustam a quantidade de raios
                elif evento.key == pygame.K_RIGHT:
                    PSY_RAIOS_QTD = min(PSY_RAIOS_MAX, PSY_RAIOS_QTD + 2)
                    print(f"[Cena 2] Raios: {PSY_RAIOS_QTD}")

                elif evento.key == pygame.K_LEFT:
                    PSY_RAIOS_QTD = max(PSY_RAIOS_MIN, PSY_RAIOS_QTD - 2)
                    print(f"[Cena 2] Raios: {PSY_RAIOS_QTD}")

                elif evento.key == pygame.K_6:
                    PSY_CIRCULO_ESPACO = min(PSY_CIRCULO_ESPACO + 2, PSY_CIRCULO_ESPACO_MAX)
                    print(f"[Cena 2] Espaçamento círculos: {PSY_CIRCULO_ESPACO}")
                    
                elif evento.key == pygame.K_4:
                    PSY_CIRCULO_ESPACO = max(PSY_CIRCULO_ESPACO - 2, PSY_CIRCULO_ESPACO_MIN)
                    print(f"[Cena 2] Espaçamento círculos: {PSY_CIRCULO_ESPACO}")
    return True


# ---------------- CENA 1 ----------------
def cena1():
    global angulo_rotacao, ultimo_tempo_cor, ultimo_tempo_objeto, indice_cor
    angulo_rotacao += velocidade_rotacao
    tempo_atual = time.time()
    if modo_aleatorio:
        if tempo_atual - ultimo_tempo_cor >= VELOCIDADE_TROCA_COR:
            indice_cor = random.randint(0, len(CORES) - 1)
            ultimo_tempo_cor = tempo_atual
        if tempo_atual - ultimo_tempo_objeto >= INTERVALO_GERACAO_OBJETOS:
            gerar_objeto_aleatorio()
            ultimo_tempo_objeto = tempo_atual

    tela.fill(CORES[indice_cor])
    desenhar_formas()


# ---------------- CENA 2 (GLITCH + PSICODELIA) ----------------
def construir_psicodelia_surface(w, h, t):
    """
    Constrói um Surface com elementos psicodélicos:
    - Anéis concêntricos com cores em loop (HSV -> RGB).
    - Raios (linhas) girando a partir do centro.
    """
    surf = pygame.Surface((w, h), pygame.SRCALPHA).convert_alpha()
    cx, cy = w // 2, h // 2

    # Fundo escuro semi-transparente para persistência leve (rastro)
    fade = pygame.Surface((w, h), pygame.SRCALPHA)
    fade.fill((0, 0, 0, 60))
    surf.blit(fade, (0, 0))

    # Assegura que o espaçamento nunca zere
    espacamento = max(PSY_CIRCULO_ESPACO_MIN, min(PSY_CIRCULO_ESPACO, PSY_CIRCULO_ESPACO_MAX))

    # Anéis concêntricos
    max_r = int(math.hypot(w, h) / 2) + 40
    base_h = (t * 0.12) % 1.0
    for r in range(espacamento, max_r, espacamento):
        hue = (base_h + r * 0.004) % 1.0
        cor = hsv_para_rgb(hue, 1.0, 1.0)
        pygame.draw.circle(surf, (*cor, 130), (cx, cy), r, PSY_ARCO_RAIOS)

    # Raios girando
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

def aplicar_rgb_split(base_surf, split_px):
    """
    Aplica separação de canais RGB (chromatic aberration) com pequenos offsets.
    """
    w, h = base_surf.get_size()
    out = pygame.Surface((w, h), pygame.SRCALPHA).convert_alpha()
    out.fill((0, 0, 0, 255))

    # Cópias por canal
    r_s = base_surf.copy()
    g_s = base_surf.copy()
    b_s = base_surf.copy()

    # Multiplica cada canal
    r_s.fill((255, 0, 0), special_flags=pygame.BLEND_MULT)
    g_s.fill((0, 255, 0), special_flags=pygame.BLEND_MULT)
    b_s.fill((0, 0, 255), special_flags=pygame.BLEND_MULT)

    # Offsets com pequena aleatoriedade
    ox = split_px + random.randint(-1, 1)
    oy = random.randint(-1, 1)

    out.blit(r_s, (-ox, 0), special_flags=pygame.BLEND_ADD)
    out.blit(g_s, (0, oy),   special_flags=pygame.BLEND_ADD)
    out.blit(b_s, (ox, -oy), special_flags=pygame.BLEND_ADD)

    return out

def aplicar_glitch_slices(surf, intensidade):
    """
    Aplica deslocamentos horizontais (slice glitch) em faixas aleatórias.
    """
    w, h = surf.get_size()
    slices = max(2, int(6 * intensidade) + random.randint(0, 4))
    max_offset = int(40 * intensidade) + 6

    for _ in range(slices):
        y = random.randint(0, h - 1)
        faixa_h = random.randint(6, int(30 + 60 * intensidade))
        y = min(y, max(0, h - faixa_h))
        dx = random.randint(-max_offset, max_offset)

        rect = pygame.Rect(0, y, w, faixa_h)
        faixa = surf.subsurface(rect).copy()
        surf.blit(faixa, (dx, y))

        # Algumas faixas também recebem variação de brilho
        if random.random() < 0.3 + 0.4 * intensidade:
            overlay = pygame.Surface((w, faixa_h), pygame.SRCALPHA)
            overlay.fill((random.randint(150, 255),
                          random.randint(150, 255),
                          random.randint(150, 255), int(40 + 80 * intensidade)))
            surf.blit(overlay, (0, y), special_flags=pygame.BLEND_ADD)

    return surf

def cena2():
    """
    Cena 2:
    - Gera um fundo psicodélico animado (anéis + raios giratórios).
    - Aplica separação RGB.
    - Em intervalos controlados, aplica glitch de fatias.
    - Intervalo do glitch e quantidade de raios são ajustáveis (↑/↓ e ←/→).
    - Tecla R: auto-modula PSY_RAIOS_QTD e PSY_CIRCULO_ESPACO (vai e volta).
    """
    global proximo_glitch, ultimo_auto_mod_tempo, PSY_RAIOS_QTD, PSY_CIRCULO_ESPACO
    global raios_direcao, espaco_direcao

    w, h = tela.get_size()
    t = time.time() - tempo_base_cena2

    # --- Auto-modulação (R) ---
    agora = time.time()
    if auto_psy_modulacao and (agora - ultimo_auto_mod_tempo) >= AUTO_MOD_INTERVALO:
        # Modula PSY_RAIOS_QTD
        PSY_RAIOS_QTD += AUTO_RAIOS_STEP * raios_direcao
        if PSY_RAIOS_QTD >= PSY_RAIOS_MAX:
            PSY_RAIOS_QTD = PSY_RAIOS_MAX
            raios_direcao = -1
        elif PSY_RAIOS_QTD <= PSY_RAIOS_MIN:
            PSY_RAIOS_QTD = PSY_RAIOS_MIN
            raios_direcao = 1

        # Modula PSY_CIRCULO_ESPACO
        PSY_CIRCULO_ESPACO += AUTO_ESPACO_STEP * espaco_direcao
        if PSY_CIRCULO_ESPACO >= PSY_CIRCULO_ESPACO_MAX:
            PSY_CIRCULO_ESPACO = PSY_CIRCULO_ESPACO_MAX
            espaco_direcao = -1
        elif PSY_CIRCULO_ESPACO <= PSY_CIRCULO_ESPACO_MIN:
            PSY_CIRCULO_ESPACO = PSY_CIRCULO_ESPACO_MIN
            espaco_direcao = 1

        ultimo_auto_mod_tempo = agora

    # 1) Constrói base psicodélica
    base = construir_psicodelia_surface(w, h, t)

    # 2) Aplica RGB split (chromatic aberration)
    split_px = max(1, int(RGB_SPLIT_PX * (0.6 + 0.8 * GLITCH_INTENSIDADE)))
    out = aplicar_rgb_split(base, split_px)

    # 3) Glitch por fatias em intervalos controlados
    now = time.time()
    if now >= proximo_glitch:
        out = aplicar_glitch_slices(out, GLITCH_INTENSIDADE)
        agendar_proximo_glitch(now)

    # 4) Ruído em pequenos blocos semi-transparentes (ocasional)
    ruido_qtd = int(20 * GLITCH_INTENSIDADE)
    for _ in range(ruido_qtd):
        if random.random() < 0.15 + 0.25 * GLITCH_INTENSIDADE:
            rw = random.randint(4, 18)
            rh = random.randint(2, 12)
            rx = random.randint(0, w - rw)
            ry = random.randint(0, h - rh)
            cor = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(30, 90))
            pygame.draw.rect(out, cor, (rx, ry, rw, rh))

    tela.fill((0, 0, 0))
    tela.blit(out, (0, 0))


# ---------------- CENA 3 (placeholder) ----------------
def cena3():
    tela.fill((20, 20, 20))
    fonte = pygame.font.SysFont(None, 60)
    sub = pygame.font.SysFont(None, 28)
    texto = fonte.render("Cena 3 - Em desenvolvimento", True, (250, 250, 250))
    dica = sub.render("Use 1/2/3 para alternar cenas", True, (190, 190, 190))
    tela.blit(texto, (max(20, LARGURA // 2 - texto.get_width() // 2), ALTURA // 2 - 40))
    tela.blit(dica, (max(20, LARGURA // 2 - dica.get_width() // 2), ALTURA // 2 + 20))


# ---------------- LOOP PRINCIPAL ----------------
executando = True
while executando:
    executando = processar_eventos()

    if cena_atual == 1:
        cena1()
    elif cena_atual == 2:
        cena2()
    elif cena_atual == 3:
        cena3()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
