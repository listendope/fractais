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

# -----------------------------
# Estado global da Cena 1
# -----------------------------
indice_cor = 0               # índice da cor atual
velocidade_zoom = 0.2        # fator de zoom
centro = [480, 300]          # centro inicial
angulo_rotacao = 0           # ângulo de rotação atual
velocidade_rotacao = 0       # velocidade de rotação por frame
modo_aleatorio = False       # alterna comportamento automático

ultimo_tempo_cor = time.time()      # controle da troca automática de cores
ultimo_tempo_objeto = time.time()   # controle da geração automática de objetos

# Listas de formas
circulos, quadrados, triangulos = [], [], []


# -----------------------------
# Inicialização da cena
# -----------------------------
def init_scene(largura, altura):
    """
    Ajusta o centro da cena ao iniciar ou redimensionar a janela.
    """
    global centro
    centro = [largura // 2, altura // 2]
    # print(f"[Cena 1] Centro ajustado: {tuple(centro)}")  # opcional para debug


# -----------------------------
# Tratamento de eventos
# -----------------------------
def handle_event(evento, tela):
    """
    Processa os eventos da cena 1:
    - Teclas de setas: troca de cor e zoom
    - C/Q/T: adiciona formas no centro
    - Espaço: reposiciona centro aleatoriamente
    - A/S/D: controla rotação
    - R: alterna modo aleatório
    """
    global indice_cor, velocidade_zoom, centro, velocidade_rotacao, angulo_rotacao, modo_aleatorio

    if evento.type != pygame.KEYDOWN:
        return

    # -----------------------------
    # Troca de cor com setas esquerda/direita
    # -----------------------------
    if evento.key == pygame.K_RIGHT:
        indice_cor = (indice_cor + 1) % len(CORES)
        print(f"[Cena 1] Cor -> {indice_cor}: {CORES[indice_cor]}")
    elif evento.key == pygame.K_LEFT:
        indice_cor = (indice_cor - 1) % len(CORES)
        print(f"[Cena 1] Cor <- {indice_cor}: {CORES[indice_cor]}")

    # -----------------------------
    # Zoom com setas cima/baixo
    # -----------------------------
    elif evento.key == pygame.K_UP:
        velocidade_zoom += 0.01
        print(f"[Cena 1] Zoom AUMENTOU: {velocidade_zoom:.3f}")
    elif evento.key == pygame.K_DOWN:
        velocidade_zoom -= 0.01
        print(f"[Cena 1] Zoom DIMINUIU: {velocidade_zoom:.3f}")

    # -----------------------------
    # Adição de formas no centro
    # -----------------------------
    elif evento.key == pygame.K_w:  # círculo
        circulos.append({'raio': 1, 'pos': tuple(centro)})
        print(f"[Cena 1] +Círculo no centro {tuple(centro)} | Totais: C={len(circulos)} Q={len(quadrados)} T={len(triangulos)}")
    elif evento.key == pygame.K_q:  # quadrado
        quadrados.append({'lado': 1, 'pos': tuple(centro)})
        print(f"[Cena 1] +Quadrado no centro {tuple(centro)} | Totais: C={len(circulos)} Q={len(quadrados)} T={len(triangulos)}")
    elif evento.key == pygame.K_e:  # triângulo
        triangulos.append({'tamanho': 1, 'pos': tuple(centro)})
        print(f"[Cena 1] +Triângulo no centro {tuple(centro)} | Totais: C={len(circulos)} Q={len(quadrados)} T={len(triangulos)}")

    # -----------------------------
    # Reposicionamento aleatório do centro
    # -----------------------------
    elif evento.key == pygame.K_SPACE:
        w, h = tela.get_size()
        centro = [random.randint(0, w), random.randint(0, h)]
        print(f"[Cena 1] Centro reposicionado aleatoriamente: {tuple(centro)}")

    # -----------------------------
    # Controle de rotação
    # -----------------------------
    elif evento.key == pygame.K_d:  # horária
        velocidade_rotacao = velocidade_zoom
        print(f"[Cena 1] Rotação horária: {velocidade_rotacao:.3f} (graus/frame)")
    elif evento.key == pygame.K_a:  # anti-horária
        velocidade_rotacao = -velocidade_zoom
        print(f"[Cena 1] Rotação anti-horária: {velocidade_rotacao:.3f} (graus/frame)")
    elif evento.key == pygame.K_s:  # reset
        velocidade_rotacao = 0
        angulo_rotacao = 0
        print("[Cena 1] Rotação resetada (0)")

    # -----------------------------
    # Modo aleatório
    # -----------------------------
    elif evento.key == pygame.K_r:
        modo_aleatorio = not modo_aleatorio
        estado = "ATIVADO" if modo_aleatorio else "DESATIVADO"
        print(f"[Cena 1] Modo aleatório {estado}")


# -----------------------------
# Atualização e desenho da cena
# -----------------------------
def update_and_draw(tela):
    """
    Atualiza os estados da cena e desenha todas as formas.
    """
    global angulo_rotacao, ultimo_tempo_cor, ultimo_tempo_objeto, indice_cor

    # Atualiza rotação
    angulo_rotacao += velocidade_rotacao

    tempo_atual = time.time()

    if modo_aleatorio:
        # Troca automática de cor
        if tempo_atual - ultimo_tempo_cor >= VELOCIDADE_TROCA_COR:
            indice_cor = random.randint(0, len(CORES) - 1)
            ultimo_tempo_cor = tempo_atual
            print(f"[Cena 1] (Auto) Nova cor: {indice_cor} {CORES[indice_cor]}")

        # Geração automática de objetos
        if tempo_atual - ultimo_tempo_objeto >= INTERVALO_GERACAO_OBJETOS:
            w, h = tela.get_size()
            gerar_objeto_aleatorio(circulos, quadrados, triangulos, w, h)
            ultimo_tempo_objeto = tempo_atual
            print(f"[Cena 1] (Auto) Gerado objeto | Totais: C={len(circulos)} Q={len(quadrados)} T={len(triangulos)}")

    # Preenche fundo e desenha formas
    tela.fill(CORES[indice_cor])
    desenhar_formas(tela, circulos, quadrados, triangulos, velocidade_zoom, angulo_rotacao)
