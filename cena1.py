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
    # (opcional) print ao iniciar/redimensionar
    # print(f"[Cena 1] Centro ajustado: {tuple(centro)}")

def handle_event(evento, tela):
    """Controles da cena 1 (mesmos do código original) com logs no console."""
    global indice_cor, velocidade_zoom, centro, velocidade_rotacao, angulo_rotacao, modo_aleatorio

    if evento.type != pygame.KEYDOWN:
        return

    # Troca de cor (setas esquerda/direita)
    if evento.key == pygame.K_RIGHT:
        indice_cor = (indice_cor + 1) % len(CORES)
        print(f"[Cena 1] Cor → {indice_cor}: {CORES[indice_cor]}")
    elif evento.key == pygame.K_LEFT:
        indice_cor = (indice_cor - 1) % len(CORES)
        print(f"[Cena 1] Cor ← {indice_cor}: {CORES[indice_cor]}")

    # Zoom (setas cima/baixo)
    elif evento.key == pygame.K_UP:
        velocidade_zoom += 0.01
        print(f"[Cena 1] Zoom AUMENTOU: {velocidade_zoom:.3f}")
    elif evento.key == pygame.K_DOWN:
        velocidade_zoom -= 0.01
        print(f"[Cena 1] Zoom DIMINUIU: {velocidade_zoom:.3f}")

    # Adição de formas no centro (C/Q/T)
    elif evento.key == pygame.K_w:  # círculo
        circulos.append({'raio': 1, 'pos': tuple(centro)})
        print(f"[Cena 1] +Círculo no centro {tuple(centro)} | Total: C={len(circulos)} Q={len(quadrados)} T={len(triangulos)}")
    elif evento.key == pygame.K_q:  # quadrado
        quadrados.append({'lado': 1, 'pos': tuple(centro)})
        print(f"[Cena 1] +Quadrado no centro {tuple(centro)} | Total: C={len(circulos)} Q={len(quadrados)} T={len(triangulos)}")
    elif evento.key == pygame.K_e:  # triângulo
        triangulos.append({'tamanho': 1, 'pos': tuple(centro)})
        print(f"[Cena 1] +Triângulo no centro {tuple(centro)} | Total: C={len(circulos)} Q={len(quadrados)} T={len(triangulos)}")

    # Centro aleatório (espaço)
    elif evento.key == pygame.K_SPACE:
        w, h = tela.get_size()
        centro = [random.randint(0, w), random.randint(0, h)]
        print(f"[Cena 1] Centro reposicionado aleatoriamente: {tuple(centro)}")

    # Rotação (4/5/6)
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

    # Modo aleatório (R)
    elif evento.key == pygame.K_r:
        modo_aleatorio = not modo_aleatorio
        estado = "ATIVADO" if modo_aleatorio else "DESATIVADO"
        print(f"[Cena 1] Modo aleatório {estado} (troca de cor periódica e geração de objetos)")

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
            # Log opcional para ver a troca automática:
            # print(f"[Cena 1] (Auto) Nova cor: {indice_cor} {CORES[indice_cor]}")

        # geração periódica de objetos
        if tempo_atual - ultimo_tempo_objeto >= INTERVALO_GERACAO_OBJETOS:
            w, h = tela.get_size()
            gerar_objeto_aleatorio(circulos, quadrados, triangulos, w, h)
            ultimo_tempo_objeto = tempo_atual
            # Log opcional para ver a geração automática:
            # print(f"[Cena 1] (Auto) Gerado objeto | Totais: C={len(circulos)} Q={len(quadrados)} T={len(triangulos)}")

    # fundo e formas
    tela.fill(CORES[indice_cor])
    # ordem dos parâmetros: (tela, circulos, quadrados, triangulos, velocidade_zoom, angulo_rotacao)
    desenhar_formas(tela, circulos, quadrados, triangulos, velocidade_zoom, angulo_rotacao)
