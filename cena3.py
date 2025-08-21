import pygame
import random
import math
import time

# =========================
# Parâmetros ajustáveis
# =========================
STAR_COUNT = 800        # quantidade de estrelas
SPEED = 0.12            # "velocidade base" (ajustada com dt para ficar estável)
DEPTH = 32.0            # profundidade máxima (z)
TRAIL = True            # rastro ligado/desligado
LINE = True             # desenhar como linha (True) ou ponto (False)

# Fade baseado em half-life:
# em FADE_HALF_LIFE segundos, a intensidade/persistência do rastro cai pela metade.
FADE_HALF_LIFE = 0.35   # segundos (0 => "apagão" completo por frame)
MOVE_SPEED = 420        # px/seg para WASD mover o centro do efeito

# =========================
# Estado interno
# =========================
_stars = []             # cada estrela: {"x":float,"y":float,"z":float, "px":int|None,"py":int|None}
_last_time = None       # para calcular dt
_center_offset = [0.0, 0.0]  # deslocamento do centro (WASD)
_keys = {"w": False, "a": False, "s": False, "d": False}

# =========================
# Utilitários
# =========================
def _rand_on_unit_disk():
    """Ponto aleatório uniforme dentro de um disco unitário (raio <= 1)."""
    ang = random.random() * 2.0 * math.pi
    # sqrt para uniformidade radial
    r = math.sqrt(random.random())
    return r * math.cos(ang), r * math.sin(ang)

def _new_star(z=None):
    x, y = _rand_on_unit_disk()
    return {"x": x, "y": y, "z": z if z is not None else random.uniform(0.5, DEPTH),
            "px": None, "py": None}

def _ensure_star_count(n):
    global _stars
    cur = len(_stars)
    if cur < n:
        _stars.extend(_new_star() for _ in range(n - cur))
    elif cur > n:
        _stars = _stars[:n]

def _reset_field():
    global _stars
    _stars = []
    _ensure_star_count(STAR_COUNT)

def init_scene(largura=None, altura=None):
    """Chame no início ou em redimensionamentos (se desejar)."""
    global _center_offset, _last_time
    _center_offset = [0.0, 0.0]
    _reset_field()
    _last_time = None  # reinicia dt

def handle_event(evento):
    """Controles:
       ↑/↓  : velocidade
       ←/→  : quantidade de estrelas
       R    : reset
       Espaço: liga/desliga rastro
       L    : alterna ponto/linha
       W/A/S/D: move o centro (manter pressionado)
       q/e  : diminui/aumenta half-life do fade
    """
    global SPEED, STAR_COUNT, TRAIL, LINE, FADE_HALF_LIFE

    # Estado de teclas para WASD (suporte a hold)
    if evento.type == pygame.KEYDOWN or evento.type == pygame.KEYUP:
        is_down = (evento.type == pygame.KEYDOWN)
        if evento.key == pygame.K_w: _keys["w"] = is_down
        if evento.key == pygame.K_a: _keys["a"] = is_down
        if evento.key == pygame.K_s: _keys["s"] = is_down
        if evento.key == pygame.K_d: _keys["d"] = is_down

    if evento.type != pygame.KEYDOWN:
        return

    if evento.key == pygame.K_UP:
        SPEED = min(2.0, SPEED + 0.01)
        print(f"[Cena 3] Velocidade: {SPEED:.3f}")

    elif evento.key == pygame.K_DOWN:
        SPEED = max(0.01, SPEED - 0.01)
        print(f"[Cena 3] Velocidade: {SPEED:.3f}")

    elif evento.key == pygame.K_RIGHT:
        STAR_COUNT = min(4000, STAR_COUNT + 80)
        _ensure_star_count(STAR_COUNT)
        print(f"[Cena 3] Estrelas: {STAR_COUNT}")

    elif evento.key == pygame.K_LEFT:
        STAR_COUNT = max(50, STAR_COUNT - 80)
        _ensure_star_count(STAR_COUNT)
        print(f"[Cena 3] Estrelas: {STAR_COUNT}")

    elif evento.key == pygame.K_r:
        init_scene()
        print("[Cena 3] Campo de estrelas resetado.")

    elif evento.key == pygame.K_SPACE:
        TRAIL = not TRAIL
        print(f"[Cena 3] Rastro: {'ATIVADO' if TRAIL else 'DESATIVADO'}")

    elif evento.key == pygame.K_l:
        LINE = not LINE
        print(f"[Cena 3] Linhas: {'ATIVADAS' if LINE else 'DESATIVADAS'}")

    elif evento.key == pygame.K_e:
        FADE_HALF_LIFE = min(2.5, FADE_HALF_LIFE + 0.05)
        print(f"[Cena 3] Fade half-life: {FADE_HALF_LIFE:.2f}s (mais persistente)")

    elif evento.key == pygame.K_q:
        FADE_HALF_LIFE = max(0.0, FADE_HALF_LIFE - 0.05)
        print(f"[Cena 3] Fade half-life: {FADE_HALF_LIFE:.2f}s (desaparece mais rápido)")

def _project_star(star, center_x, center_y, scale):
    """Projeção 3D -> 2D em perspectiva, com centro deslocável."""
    z = max(0.001, star["z"])
    sx = int(center_x + (star["x"] / z) * scale)
    sy = int(center_y + (star["y"] / z) * scale)
    return sx, sy

def _apply_fade(tela, dt):
    """Fade com half-life dependente do dt: após 'FADE_HALF_LIFE' s, a intensidade cai pela metade."""
    if not TRAIL:
        tela.fill((0, 0, 0))
        return
    # FADE_HALF_LIFE == 0 -> apagar muito forte (sem rastro)
    if FADE_HALF_LIFE <= 0.0:
        fade_alpha = 255
    else:
        # intensidade que permanece após dt
        # restante = 0.5 ** (dt / half_life), então alpha_norm = 1 - restante
        alpha_norm = 1.0 - pow(0.5, dt / FADE_HALF_LIFE)
        fade_alpha = max(0, min(255, int(255 * alpha_norm)))

    w, h = tela.get_size()
    fade = pygame.Surface((w, h), pygame.SRCALPHA)
    fade.fill((0, 0, 0, fade_alpha))
    tela.blit(fade, (0, 0))

def cena3(tela):
    """Atualiza e desenha a Cena 3 (starfield com fade aprimorado e centro WASD)."""
    global _last_time

    # dt independente de FPS
    now = time.time()
    if _last_time is None:
        dt = 0.0
    else:
        dt = max(0.0, min(0.1, now - _last_time))  # clamp para estabilidade
    _last_time = now

    # Tela & centro
    w, h = tela.get_size()
    cx, cy = w // 2, h // 2
    cx += int(_center_offset[0])
    cy += int(_center_offset[1])
    scale = min(w, h) * 0.9

    # Inicializa campo se necessário
    if not _stars:
        _reset_field()

    # Move o centro com WASD (suporta manter pressionado)
    move_x = (1 if _keys["d"] else 0) - (1 if _keys["a"] else 0)
    move_y = (1 if _keys["s"] else 0) - (1 if _keys["w"] else 0)
    if move_x or move_y:
        _center_offset[0] += move_x * MOVE_SPEED * dt
        _center_offset[1] += move_y * MOVE_SPEED * dt

    # Fade com half-life dependente de dt
    _apply_fade(tela, dt)

    # Atualiza e desenha estrelas
    for star in _stars:
        # Inicializa ponto anterior para linhas
        if LINE and (star["px"] is None or star["py"] is None):
            px, py = _project_star(star, cx, cy, scale)
            star["px"], star["py"] = px, py

        # Avanço em z (independente de FPS)
        star["z"] -= SPEED * dt * 60.0  # 60.0 ajuda a manter sensação parecida com step fixo

        # Reposiciona quando chega muito perto da câmera
        if star["z"] <= 0.05:
            new = _new_star(DEPTH)
            star.update(new)
            continue

        sx, sy = _project_star(star, cx, cy, scale)

        # Fora da tela -> reaparece ao fundo
        if sx < -10 or sx > w + 10 or sy < -10 or sy > h + 10:
            new = _new_star(DEPTH)
            star.update(new)
            continue

        # Brilho/tamanho proporcionais à proximidade
        t = max(0.0, min(1.0, 1.0 - (star["z"] / DEPTH)))
        size = 1 + int(3 * t)
        col = 150 + int(105 * t)
        color = (col, col, col)

        if LINE and star["px"] is not None and star["py"] is not None:
            pygame.draw.line(tela, color, (star["px"], star["py"]), (sx, sy), max(1, size - 1))
        else:
            pygame.draw.circle(tela, color, (sx, sy), size)

        # Atualiza ponto anterior
        star["px"], star["py"] = sx, sy
