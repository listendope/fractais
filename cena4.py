import pygame
import colorsys
import time
from utils import rotacionar_ponto

# =======================
# Configurações gerais
# =======================
FONT_SIZE = 100
TEXTO = " DOPE "
NUM_FAIXAS = 5
SPEED = 1

# BPM e subdivisão do strobe
BPM = 130
SUBDIVISAO = 2
strobe_interval = 60.0 / (BPM * SUBDIVISAO)

# =======================
# Estado da cena
# =======================
_font = None
_text_surface_base = None
_text_w = 0
_text_h = 0

_offsets = [0 for _ in range(NUM_FAIXAS)]
psy_mode = False
strobe_mode = False
hue = 0.0

last_strobe_time = time.time()
strobe_on = False

# Animação de faixas
anim_start_time = None
anim_duration = 10.0
anim_active = False
anim_direction = 1  # 1=subindo (1→10), -1=descendo (10→1)

# Rotação
rotacao_angulo = 0.0
rotacao_vel = 0.5
rotacao_direcao = 0  # -1=anti-horário, 1=horário, 0=parado


# =======================
# Funções auxiliares
# =======================
def _ensure_font():
    """Garante que a fonte e a superfície base estejam inicializadas."""
    global _font, _text_surface_base, _text_w, _text_h
    if _font is None:
        if not pygame.font.get_init():
            pygame.font.init()
        _font = pygame.font.SysFont("Arial Black", FONT_SIZE, bold=True)
        _text_surface_base = _font.render(f" {TEXTO} ", True, (255, 255, 255))
        _text_w = _text_surface_base.get_width()
        _text_h = _text_surface_base.get_height()

def _update_strobe_interval():
    """Atualiza o intervalo de strobe com base no BPM atual."""
    global strobe_interval
    strobe_interval = 60.0 / (BPM * SUBDIVISAO)

def interpolate_offsets(old_offsets, new_count):
    """Interpola offsets antigos para se ajustar ao novo número de faixas."""
    old_count = len(old_offsets)
    if old_count == 0:
        return [0 for _ in range(new_count)]
    new_offsets = []
    for i in range(new_count):
        rel = i / max(new_count - 1, 1)
        idx_float = rel * (old_count - 1)
        idx0 = int(idx_float)
        idx1 = min(idx0 + 1, old_count - 1)
        frac = idx_float - idx0
        val = old_offsets[idx0] * (1 - frac) + old_offsets[idx1] * frac
        new_offsets.append(val)
    return new_offsets

def update_anim():
    """Atualiza NUM_FAIXAS com curva parabólica slow-fast-slow e interpola offsets."""
    global NUM_FAIXAS, _offsets, anim_start_time, anim_active, anim_direction

    if not anim_active:
        return

    t = (time.time() - anim_start_time) / anim_duration
    if t >= 1.0:
        t = 1.0
        anim_direction *= -1  # inverte sentido
        anim_start_time = time.time()

    # Curva parabólica slow-fast-slow
    curva = -4 * (t - 0.5) ** 2 + 1
    curva_normalizada = (curva + 1) / 2

    if anim_direction == 1:
        num = int(1 + curva_normalizada * (10 - 1))
    else:
        num = int(10 - curva_normalizada * (10 - 1))

    if num != NUM_FAIXAS:
        _offsets = interpolate_offsets(_offsets, num)
        NUM_FAIXAS = num


# =======================
# Controle de eventos
# =======================
def handle_event(evento, tela=None):
    """Gerencia teclas de controle da cena 4."""
    global psy_mode, strobe_mode, BPM, NUM_FAIXAS, _offsets
    global anim_start_time, anim_active, anim_direction
    global rotacao_direcao, rotacao_angulo

    if evento.type != pygame.KEYDOWN:
        return

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
    elif evento.key == pygame.K_DOWN and BPM > 1:
        BPM -= 1
        _update_strobe_interval()
        print(f"[Cena 4] BPM: {BPM}")
    elif evento.key == pygame.K_RIGHT:
        NUM_FAIXAS = min(10, NUM_FAIXAS + 1)
        _offsets = interpolate_offsets(_offsets, NUM_FAIXAS)
        print(f"[Cena 4] Faixas: {NUM_FAIXAS}")
    elif evento.key == pygame.K_LEFT:
        NUM_FAIXAS = max(1, NUM_FAIXAS - 1)
        _offsets = interpolate_offsets(_offsets, NUM_FAIXAS)
        print(f"[Cena 4] Faixas: {NUM_FAIXAS}")
    elif evento.key == pygame.K_a:
        anim_active = not anim_active
        if anim_active:
            anim_start_time = time.time()
            anim_direction = 1
            print("[Cena 4] Animação de faixas ativada")
        else:
            print("[Cena 4] Animação de faixas desativada")
    elif evento.key == pygame.K_q:
        rotacao_direcao = -1
        print(f"[Cena 4] Rotação anti-horária: {rotacao_vel} (graus/frame)")
    elif evento.key == pygame.K_e:
        rotacao_direcao = 1
        print(f"[Cena 4] Rotação horária: {rotacao_vel} (graus/frame)")
    elif evento.key == pygame.K_w:
        rotacao_direcao = 0
        rotacao_angulo = 0.0
        print("[Cena 4] Rotação resetada (0)")


# =======================
# Cena principal
# =======================
def cena4(tela):
    """Render principal da Cena 4: texto psicodélico + strobe + rotação."""
    global hue, last_strobe_time, strobe_on, rotacao_angulo, rotacao_direcao

    _ensure_font()
    update_anim()

    largura, altura = tela.get_size()
    faixa_altura = altura // NUM_FAIXAS
    rotacao_angulo += rotacao_direcao * rotacao_vel

    # --- Fundo (strobe) ---
    background_color = (0, 0, 0)
    if strobe_mode:
        now = time.time()
        if now - last_strobe_time >= strobe_interval:
            strobe_on = not strobe_on
            last_strobe_time = now
        background_color = (255, 255, 255) if strobe_on else (232, 104, 0)

    tela.fill(background_color)

    # --- Desenha faixas com rotação ---
    centro_x, centro_y = largura / 2, altura / 2
    for i in range(NUM_FAIXAS):
        y = i * faixa_altura + (faixa_altura - _text_h) // 2

        # Alterna direção de deslocamento
        direction = -1 if i % 2 == 0 else 1
        _offsets[i] = (_offsets[i] + direction * SPEED) % _text_w

        # Cor do texto
        if psy_mode:
            hue = (hue + 0.002) % 1.0
            r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb((hue + i * 0.15) % 1.0, 1, 1)]
            text_surface = _font.render(f" {TEXTO} ", True, (r, g, b))
        elif strobe_mode:
            cor = (232, 104, 0) if background_color == (255, 255, 255) else (255, 255, 255)
            text_surface = _font.render(f" {TEXTO} ", True, cor)
        else:
            text_surface = _text_surface_base

        # Desenha repetidamente ao longo da tela
        for x0 in (_offsets[i], _offsets[i] - _text_w):
            x = x0
            while x < largura:
                pos = rotacionar_ponto(x, y, centro_x, centro_y, rotacao_angulo)
                tela.blit(text_surface, pos)
                x += _text_w
