import math
import random
import time
import colorsys
import pygame

# =========================
# Constantes gerais
# =========================
LARGURA, ALTURA = 960, 600
FPS = 240

CORES = [
    (255, 0, 0),      # vermelho
    (0, 255, 0),      # verde
    (0, 0, 255),      # azul
    (255, 255, 0),    # amarelo
    (128, 0, 128),    # roxo
    (255, 165, 0),    # laranja
    (0, 255, 255),    # ciano
    (255, 192, 203),  # rosa
    (0, 0, 0)         # preto
]

VELOCIDADE_TROCA_COR = 0.2
INTERVALO_GERACAO_OBJETOS = 0.5

# =========================
# Funções auxiliares
# =========================
def rotacionar_ponto(x, y, cx, cy, angulo):
    """Rotaciona um ponto (x, y) em torno do centro (cx, cy) por um ângulo em graus."""
    rad = math.radians(angulo)
    cos_a, sin_a = math.cos(rad), math.sin(rad)
    dx, dy = x - cx, y - cy
    return dx * cos_a - dy * sin_a + cx, dx * sin_a + dy * cos_a + cy

def hsv_para_rgb(h, s, v):
    """Converte valores HSV em RGB (0-255)."""
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return int(r*255), int(g*255), int(b*255)

# =========================
# Desenho de formas
# =========================
def desenhar_formas(tela, circulos, quadrados, triangulos, velocidade_zoom, angulo_rotacao):
    """Desenha e atualiza objetos geométricos com crescimento e rotação."""
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

def gerar_objeto_aleatorio(circulos, quadrados, triangulos, largura, altura):
    """Gera um objeto aleatório (círculo, quadrado ou triângulo) em uma posição aleatória."""
    tipo = random.choice(['c', 'q', 't'])
    pos = (random.randint(0, largura), random.randint(0, altura))
    if tipo == 'c':
        circulos.append({'raio': 1, 'pos': pos})
    elif tipo == 'q':
        quadrados.append({'lado': 1, 'pos': pos})
    elif tipo == 't':
        triangulos.append({'tamanho': 1, 'pos': pos})

# =========================
# Efeitos visuais
# =========================
def aplicar_rgb_split(base_surf, split_px):
    """Aplica efeito de deslocamento RGB em uma superfície."""
    w, h = base_surf.get_size()
    out = pygame.Surface((w, h), pygame.SRCALPHA).convert_alpha()
    out.fill((0, 0, 0, 255))

    # Cria camadas de cor
    r_s, g_s, b_s = base_surf.copy(), base_surf.copy(), base_surf.copy()
    r_s.fill((255,0,0), special_flags=pygame.BLEND_MULT)
    g_s.fill((0,255,0), special_flags=pygame.BLEND_MULT)
    b_s.fill((0,0,255), special_flags=pygame.BLEND_MULT)

    # Deslocamentos aleatórios
    ox = split_px + random.randint(-1, 1)
    oy = random.randint(-1, 1)

    # Combina camadas
    out.blit(r_s, (-ox, 0), special_flags=pygame.BLEND_ADD)
    out.blit(g_s, (0, oy), special_flags=pygame.BLEND_ADD)
    out.blit(b_s, (ox, -oy), special_flags=pygame.BLEND_ADD)

    return out

def aplicar_glitch_slices(surf, intensidade):
    """Aplica efeito de glitch em fatias horizontais da superfície."""
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

        # Adiciona overlay colorido aleatório
        if random.random() < 0.3 + 0.4 * intensidade:
            overlay = pygame.Surface((w, faixa_h), pygame.SRCALPHA)
            overlay.fill((random.randint(150, 255),
                          random.randint(150, 255),
                          random.randint(150, 255), int(40 + 80 * intensidade)))
            surf.blit(overlay, (0, y), special_flags=pygame.BLEND_ADD)

    return surf

def agendar_proximo_glitch(intensidade, intervalo_min, intervalo_max, intervalo_min_lim):
    """Calcula o timestamp para o próximo glitch, baseado em intensidade."""
    fator = 0.5 + intensidade
    intervalo = random.uniform(intervalo_min, intervalo_max) / fator
    return time.time() + max(intervalo_min_lim, intervalo)
