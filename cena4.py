import pygame
import colorsys
import time

# =======================
# Configurações gerais
# =======================
FONT_SIZE = 100
TEXTO = " DOPE "
NUM_FAIXAS = 5
SPEED = 1

# --- Configuração inicial de BPM e subdivisão ---
BPM = 130          # valor inicial
SUBDIVISAO = 2     # 1=1 piscada/batida, 2=2, 4=4 piscadas/batida
strobe_interval = 60.0 / (BPM * SUBDIVISAO)

# =======================
# Estado da cena
# =======================
# Fonte e superfícies (inicialização preguiçosa)
_font = None
_text_surface_base = None
_text_w = 0
_text_h = 0

# Offsets para cada faixa
_offsets = [0 for _ in range(NUM_FAIXAS)]

# Modos
psy_mode = False
strobe_mode = False
hue = 0.0

# Controle do strobe
last_strobe_time = time.time()
strobe_on = False


def _ensure_font():
    """Garante que a fonte e a superfície base estão prontas."""
    global _font, _text_surface_base, _text_w, _text_h
    if _font is None:
        if not pygame.font.get_init():
            pygame.font.init()  # evita 'font not initialized'
        _font = pygame.font.SysFont("Arial Black", FONT_SIZE, bold=True)
        _text_surface_base = _font.render(f" {TEXTO} ", True, (255, 255, 255))
        _text_w = _text_surface_base.get_width()
        _text_h = _text_surface_base.get_height()


def _update_strobe_interval():
    global strobe_interval
    strobe_interval = 60.0 / (BPM * SUBDIVISAO)


def handle_event(evento, tela=None):
    """Teclas:
        Z -> psicodelia on/off
        X -> strobe on/off
        ↑ -> BPM +1
        ↓ -> BPM -1
    """
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
            _update_strobe_interval()
            print(f"[Cena 4] BPM: {BPM}")

        elif evento.key == pygame.K_DOWN:
            if BPM > 1:
                BPM -= 1
                _update_strobe_interval()
                print(f"[Cena 4] BPM: {BPM}")


def cena4(tela):
    """Desenha a cena do telão DOPE."""
    global hue, last_strobe_time, strobe_on

    _ensure_font()

    largura, altura = tela.get_size()
    faixa_altura = altura // NUM_FAIXAS

    # Fundo (strobe)
    background_color = (0, 0, 0)
    if strobe_mode:
        now = time.time()
        if now - last_strobe_time >= strobe_interval:
            strobe_on = not strobe_on
            last_strobe_time = now
        background_color = (255, 255, 255) if strobe_on else (0, 0, 0)

    tela.fill(background_color)

    # Desenha as 5 faixas
    for i in range(NUM_FAIXAS):
        y = i * faixa_altura + (faixa_altura - _text_h) // 2

        # Direção alternada: 0,2,4 -> direita->esquerda | 1,3 -> esquerda->direita
        direction = -1 if i % 2 == 0 else 1
        _offsets[i] = (_offsets[i] + direction * SPEED) % _text_w

        # Cor do texto
        if psy_mode:
            hue = (hue + 0.002) % 1.0
            r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb((hue + i * 0.15) % 1.0, 1, 1)]
            text_surface = _font.render(f" {TEXTO} ", True, (r, g, b))
        else:
            if strobe_mode:
                # Inverte cor pra ficar visível no flash branco
                cor = (0, 0, 0) if background_color == (255, 255, 255) else (255, 255, 255)
                text_surface = _font.render(f" {TEXTO} ", True, cor)
            else:
                text_surface = _text_surface_base

        # Desenha repetidamente para preencher sem gaps
        for x0 in (_offsets[i], _offsets[i] - _text_w):
            x = x0
            while x < largura:
                tela.blit(text_surface, (x, y))
                x += _text_w
