import pygame
import random
import time
from utils import (
    rotacionar_ponto,
    desenhar_formas,
    gerar_objeto_aleatorio,
    CORES,
    VELOCIDADE_TROCA_COR,
    INTERVALO_GERACAO_OBJETOS,
)

# ----- Estado da Cena 1 -----
indice_cor = 0
velocidade_zoom = 0.2
centro = [480, 300]
angulo_rotacao = 0
velocidade_rotacao = 0
modo_aleatorio = False
ultimo_tempo_cor = time.time()
ultimo_tempo_objeto = time.time()
circulos, quadrados, triangulos = [], [], []

def init_scene(largura, altura):
    """Reposiciona o centro quando a janela redimensiona ou no início."""
    global centro
    centro = [largura // 2, altura // 2]

def handle_event(evento, tela):
    """Controles da cena 1 (mesmos do código original)."""
    global indice_cor, velocidade_zoom, centro, velocidade_rotacao, angulo_rotacao, modo_aleatorio

    if evento.type != pygame.KEYDOWN:
        return

    if evento.key == pygame.K_RIGHT:
        indice_cor = (indice_cor + 1) % len(CORES)
    elif evento.key == pygame.K_LEFT:
        indice_cor = (indice_cor - 1) % len(CORES)
    elif evento.key == pygame.K_UP:
        velocidade_zoom += 0.01
    elif evento.key == pygame.K_DOWN:
        velocidade_zoom -= 0.01
    elif evento.key == pygame.K_c:  # círculo no centro
        circulos.append({'raio': 1, 'pos': tuple(centro)})
    elif evento.key == pygame.K_q:  # quadrado no centro
        quadrados.append({'lado': 1, 'pos': tuple(centro)})
    elif evento.key == pygame.K_t:  # triângulo no centro
        triangulos.append({'tamanho': 1, 'pos': tuple(centro)})
    elif evento.key == pygame.K_SPACE:  # reposiciona o centro aleatoriamente
        w, h = tela.get_size()
        centro = [random.randint(0, w), random.randint(0, h)]
    elif evento.key == pygame.K_6:  # anti-horário
        velocidade_rotacao = velocidade_zoom
    elif evento.key == pygame.K_4:  # horário
        velocidade_rotacao = -velocidade_zoom
    elif evento.key == pygame.K_5:  # reset rotação
        velocidade_rotacao = 0
        angulo_rotacao = 0
    elif evento.key == pygame.K_r:  # modo aleatório (cor/objetos)
        modo_aleatorio = not modo_aleatorio

def update_and_draw(tela):
    """Atualiza e desenha a cena 1."""
    global angulo_rotacao, ultimo_tempo_cor, ultimo_tempo_objeto, indice_cor
    angulo_rotacao += velocidade_rotacao

    tempo_atual = time.time()
    if modo_aleatorio:
        # troca periódica de cor
        if tempo_atual - ultimo_tempo_cor >= VELOCIDADE_TROCA_COR:
            indice_cor = random.randint(0, len(CORES) - 1)
            ultimo_tempo_cor = tempo_atual
        # geração periódica de objetos
        if tempo_atual - ultimo_tempo_objeto >= INTERVALO_GERACAO_OBJETOS:
            w, h = tela.get_size()
            gerar_objeto_aleatorio(circulos, quadrados, triangulos, w, h)
            ultimo_tempo_objeto = tempo_atual

    # fundo e formas
    tela.fill(CORES[indice_cor])
    # OBS: ordem dos parâmetros: (tela, circulos, quadrados, triangulos, velocidade_zoom, angulo_rotacao)
    desenhar_formas(tela, circulos, quadrados, triangulos, velocidade_zoom, angulo_rotacao)
