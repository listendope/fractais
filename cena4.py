import pygame
import random
import math
import time

# =========================
# Parâmetros visuais
# =========================
FONT_SIZE = 36
TRACKING = -4                 # espaçamento vertical entre linhas (leading)
BASE_DROP_SPEED = 135.0       # px/seg por coluna (base), multiplicado pelo _speed_mult
COLUMN_VARIANCE = 0.28        # variação de velocidade entre colunas (0..1)
MIN_STREAM_LEN = 14           # comprimento mínimo (linhas)
MAX_STREAM_LEN = 38           # comprimento máximo (linhas)
LETTERS = ['D', 'O', 'P', 'E']  # sua marca!

# Flicker sutil (troca de alguns caracteres perto do head)
FLICKER_RATE_PER_STREAM = 10.0  # mutações/seg por coluna (aprox)
FLICKER_SPAN_FRACTION = 0.35    # fração superior da cauda onde acontece o flicker

# Fade/trilha com half-life (independente de FPS)
FADE_HALF_LIFE = 0.25           # seg (0 -> quase sem rastro; >1.2 -> trilha mais forte)

# Glow / Bloom
GLOW_ENABLED = False
GLOW_PASSES = 2                 # 1..3 (custo cresce)
GLOW_RADIUS = 2                 # px de deslocamento por passe

# Paletas (3 variações)
PALETTES = [
    {   # 0 - Matrix Green
        "bg": (0, 0, 0),
        "tail_dark": (0, 60, 18),
        "tail_mid": (0, 140, 60),
        "head": (230, 255, 230)
    },
    {   # 1 - Cyan
        "bg": (0, 0, 0),
        "tail_dark": (0, 50, 75),
        "tail_mid": (0, 180, 210),
        "head": (220, 255, 255)
    },
    {   # 2 - Magenta
        "bg": (0, 0, 0),
        "tail_dark": (70, 10, 60),
        "tail_mid": (220, 60, 200),
        "head": (255, 210, 255)
    }
]

# =========================
# Estado interno
# =========================
_current_palette = 0
_streams = []                  # lista de colunas (dicts)
_last_time = None
_paused = False
_speed_mult = 1.0
_last_size = None

# Cache de glyphs por paleta e nível de intensidade
_font = None
_CACHE = {}  # {(palette_idx, level, char): surface}

# Cada coluna: {
#   "x": float,             # POSIÇÃO FIXA X -> cai RETO
#   "y_head": float,
#   "speed": float,         # px/seg
#   "len": int,
#   "accum": float,         # px acumulado p/ avançar 1 linha
#   "chars": [list de chars],
#   "flicker_accum": float
# }

# =========================
# Utilitários
# =========================
def _mk_font():
    global _font
    if _font is None:
        _font = pygame.font.SysFont("Consolas", FONT_SIZE, bold=True)
    return _font

def _line_step():
    return max(8, FONT_SIZE + TRACKING)

def _rand_stream_len():
    return random.randint(MIN_STREAM_LEN, MAX_STREAM_LEN)

def _new_column(x, h):
    length = _rand_stream_len()
    return {
        "x": float(x),  # <- SEM SWAY: x FIXO
        "y_head": random.uniform(-h, 0),  # começa acima da tela
        "speed": BASE_DROP_SPEED * (1.0 + (random.uniform(-COLUMN_VARIANCE, COLUMN_VARIANCE))),
        "len": length,
        "accum": 0.0,
        "chars": [random.choice(LETTERS) for _ in range(length)],
        "flicker_accum": 0.0
    }

def _build_streams(w, h, columns):
    global _streams
    _streams = []
    col_w = max(1, FONT_SIZE)  # largura por coluna ~ glyph width
    max_cols = max(1, w // col_w)
    columns = max(1, min(columns, max_cols))

    total_w = columns * col_w
    start_x = (w - total_w) // 2
    for i in range(columns):
        x = start_x + i * col_w
        _streams.append(_new_column(x, h))

def _reflow_if_needed(w, h, desired_cols):
    global _last_size
    if _last_size != (w, h) or len(_streams) == 0:
        _build_streams(w, h, desired_cols)
        _last_size = (w, h)

def _desired_columns():
    return getattr(_desired_columns, "n", 52)

def _set_desired_columns(n):
    _desired_columns.n = int(n)

_set_desired_columns(52)

def _lerp(a, b, t):
    return a + (b - a) * t

def _lerp_color(c1, c2, t):
    t = max(0.0, min(1.0, t))
    return (int(_lerp(c1[0], c2[0], t)),
            int(_lerp(c1[1], c2[1], t)),
            int(_lerp(c1[2], c2[2], t)))

def _glyph_surface(palette_idx, level, ch):
    """
    Retorna um glyph pré-renderizado para o 'level' da cauda:
      level=0 -> head brilhante
      level=N-1 -> cauda mais escura
    """
    key = (palette_idx, level, ch)
    surf = _CACHE.get(key)
    if surf is not None:
        return surf

    font = _mk_font()
    pal = PALETTES[palette_idx]
    head = pal["head"]
    tail_mid = pal["tail_mid"]
    tail_dark = pal["tail_dark"]

    N = 10  # níveis de intensidade
    if level <= 0:
        color = head
    else:
        t = (level - 1) / (N - 1)  # 0..1 ao longo da cauda (exclui head)
        color = _lerp_color(tail_mid, tail_dark, t**1.12)

    surf = font.render(ch, True, color)
    _CACHE[key] = surf
    return surf

def _clear_cache():
    _CACHE.clear()

def _half_life_alpha(dt):
    if FADE_HALF_LIFE <= 0.0:
        return 255
    alpha_norm = 1.0 - pow(0.5, dt / FADE_HALF_LIFE)
    return max(0, min(255, int(255 * alpha_norm)))

def init_scene(largura=None, altura=None):
    """Reseta tudo (chame ao entrar na cena)."""
    global _last_time, _speed_mult, _paused, _current_palette, _font
    _last_time = None
    _speed_mult = 1.0
    _paused = False
    _current_palette = 0
    _font = None
    _clear_cache()
    _build_streams(largura or 960, altura or 600, _desired_columns())

# =========================
# Controles
# =========================
def handle_event(evento):
    """
    Controles:
      ↑/↓ : velocidade global
      ←/→ : número de colunas
      ESPAÇO : pausa/continua
      R : reset
      G : alterna glow
      5 : próxima paleta (cíclico)
      4/6 : diminui/aumenta persistência do rastro (half-life)
    """
    global _paused, _speed_mult, GLOW_ENABLED, _current_palette, FADE_HALF_LIFE

    if evento.type != pygame.KEYDOWN:
        return

    if evento.key == pygame.K_UP:
        _speed_mult = min(4.0, _speed_mult + 0.1)
        print(f"[Cena 4] Velocidade x{_speed_mult:.2f}")
    elif evento.key == pygame.K_DOWN:
        _speed_mult = max(0.1, _speed_mult - 0.1)
        print(f"[Cena 4] Velocidade x{_speed_mult:.2f}")

    elif evento.key == pygame.K_RIGHT:
        _set_desired_columns(_desired_columns() + 4)
        print(f"[Cena 4] Colunas: {_desired_columns()}")
    elif evento.key == pygame.K_LEFT:
        _set_desired_columns(max(4, _desired_columns() - 4))
        print(f"[Cena 4] Colunas: {_desired_columns()}")

    elif evento.key == pygame.K_SPACE:
        _paused = not _paused
        print(f"[Cena 4] {'Pausado' if _paused else 'Rodando'}")

    elif evento.key == pygame.K_r:
        init_scene()
        print("[Cena 4] Reset")

    elif evento.key == pygame.K_g:
        GLOW_ENABLED = not GLOW_ENABLED
        print(f"[Cena 4] Glow: {'ON' if GLOW_ENABLED else 'OFF'}")

    elif evento.key == pygame.K_5:
        _current_palette = (_current_palette + 1) % len(PALETTES)
        _clear_cache()
        print(f"[Cena 4] Paleta alterada para: {_current_palette}")

    elif evento.key == pygame.K_6:
        FADE_HALF_LIFE = min(3.0, FADE_HALF_LIFE + 0.05)
        print(f"[Cena 4] Fade half-life: {FADE_HALF_LIFE:.2f}s")
    elif evento.key == pygame.K_4:
        FADE_HALF_LIFE = max(0.0, FADE_HALF_LIFE - 0.05)
        print(f"[Cena 4] Fade half-life: {FADE_HALF_LIFE:.2f}s")

# =========================
# Desenho
# =========================
def _draw_glow(text_surf, target, x, y):
    """Brilho simples (múltiplos blits deslocados em aditivo)."""
    if not GLOW_ENABLED:
        return
    for p in range(GLOW_PASSES):
        r = (p + 1) * GLOW_RADIUS
        alpha = max(32, 120 - p * 40)
        glow = text_surf.copy()
        glow.set_alpha(alpha)
        for ox, oy in ((-r,0),(r,0),(0,-r),(0,r),(-r,-r),(r,-r),(-r,r),(r,r)):
            target.blit(glow, (x + ox, y + oy), special_flags=pygame.BLEND_ADD)

def cena4(tela):
    """Update/Draw da Cena 4 (Matrix Rain DOPE, colunas retas)."""
    global _last_time

    w, h = tela.get_size()
    _reflow_if_needed(w, h, _desired_columns())

    now = time.time()
    dt = 0.0 if _last_time is None else max(0.0, min(0.08, now - _last_time))
    _last_time = now

    pal = PALETTES[_current_palette]
    bg = pal["bg"]

    # Fade/trilha (independente de FPS)
    if _paused or FADE_HALF_LIFE <= 0.0:
        tela.fill(bg)
    else:
        fade_alpha = _half_life_alpha(dt)
        fade = pygame.Surface((w, h), pygame.SRCALPHA)
        fade.fill((*bg, fade_alpha))
        tela.blit(fade, (0, 0))

    if _paused:
        return

    line_step = _line_step()
    glow_layer = pygame.Surface((w, h), pygame.SRCALPHA) if GLOW_ENABLED else None

    for i, col in enumerate(_streams):
        # Avanço do head
        speed = col["speed"] * _speed_mult
        col["y_head"] += speed * dt
        col["accum"]  += speed * dt

        # Shift de 1 linha sempre que acumula
        while col["accum"] >= line_step:
            col["accum"] -= line_step
            col["chars"].insert(0, random.choice(LETTERS))
            if len(col["chars"]) > col["len"]:
                col["chars"].pop()

        # Reseta stream quando todo o tail passou da tela
        if col["y_head"] - col["len"] * line_step > h + line_step:
            _streams[i] = _new_column(col["x"], h)
            col = _streams[i]

        # Flicker (troca algumas letras próximo ao head)
        col["flicker_accum"] += dt * FLICKER_RATE_PER_STREAM
        if col["flicker_accum"] >= 1.0:
            col["flicker_accum"] -= 1.0
            span = max(2, int(col["len"] * FLICKER_SPAN_FRACTION))
            idx_mut = random.randint(0, min(span, len(col["chars"]) - 1))
            col["chars"][idx_mut] = random.choice(LETTERS)

        # Desenha tail -> head (RETO: x é FIXO)
        x = int(col["x"])
        for idx, ch in enumerate(col["chars"]):
            y = col["y_head"] - idx * line_step
            if y < -line_step or y > h + line_step:
                continue

            # Head = nível 0; tail = níveis 1..N-1
            if idx == 0:
                surf = _glyph_surface(_current_palette, 0, ch)
            else:
                N = 10
                t = idx / max(1, col["len"] - 1)
                level = 1 + int(min(N - 1, (t**1.15) * (N - 1)))
                surf = _glyph_surface(_current_palette, level, ch)

            if glow_layer is not None:
                _draw_glow(surf, glow_layer, x, int(y))

            tela.blit(surf, (x, int(y)))

    if glow_layer is not None:
        tela.blit(glow_layer, (0, 0), special_flags=pygame.BLEND_ADD)
