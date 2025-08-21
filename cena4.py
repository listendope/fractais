import pygame
import random
import time

# =========================
# Parâmetros ajustáveis
# =========================
FONT_SIZE = 32
COLUMNS = 40           # número inicial de colunas
SPEED = 180            # px/seg (velocidade da chuva)
LETTERS = ['D', 'O', 'P', 'E']
BRIGHT_COLOR = (0, 255, 70)  # verde neon
TAIL_COLOR = (0, 100, 30)    # cauda mais escura
BACKGROUND = (0, 0, 0)

# =========================
# Estado interno
# =========================
_streams = []          # lista de colunas: cada coluna é uma lista de letras com y
_last_time = None
_running = True

def _reset_streams(w, h):
    global _streams
    _streams = []
    col_width = FONT_SIZE
    num_cols = max(1, min(COLUMNS, w // col_width))
    for i in range(num_cols):
        x = i * col_width
        y_positions = [random.randint(-h, 0) for _ in range(random.randint(5, 15))]
        _streams.append({"x": x, "letters": y_positions})

def init_scene(largura=None, altura=None):
    global _last_time
    _reset_streams(largura or 800, altura or 600)
    _last_time = None

def handle_event(evento):
    global SPEED, COLUMNS, _running
    if evento.type != pygame.KEYDOWN:
        return

    if evento.key == pygame.K_UP:
        SPEED = min(600, SPEED + 20)
        print(f"[Cena 4] Velocidade: {SPEED}px/s")
    elif evento.key == pygame.K_DOWN:
        SPEED = max(20, SPEED - 20)
        print(f"[Cena 4] Velocidade: {SPEED}px/s")
    elif evento.key == pygame.K_RIGHT:
        COLUMNS = min(200, COLUMNS + 5)
        print(f"[Cena 4] Colunas: {COLUMNS}")
    elif evento.key == pygame.K_LEFT:
        COLUMNS = max(5, COLUMNS - 5)
        print(f"[Cena 4] Colunas: {COLUMNS}")
    elif evento.key == pygame.K_r:
        print("[Cena 4] Resetando chuva...")
        _reset_streams(960, 600)
    elif evento.key == pygame.K_SPACE:
        _running = not _running
        print(f"[Cena 4] {'Rodando' if _running else 'Pausado'}")

def cena4(tela):
    global _last_time
    w, h = tela.get_size()
    if not _streams:
        _reset_streams(w, h)

    now = time.time()
    if _last_time is None:
        dt = 0
    else:
        dt = now - _last_time
    _last_time = now

    tela.fill(BACKGROUND)
    font = pygame.font.SysFont("Consolas", FONT_SIZE, bold=True)

    if _running:
        for stream in _streams:
            # Atualiza posições
            for i in range(len(stream["letters"])):
                stream["letters"][i] += SPEED * dt
            # Remove letras que saíram da tela
            stream["letters"] = [y for y in stream["letters"] if y < h + FONT_SIZE]
            # Adiciona novas letras no topo
            if len(stream["letters"]) == 0 or stream["letters"][-1] > FONT_SIZE:
                stream["letters"].append(random.randint(-FONT_SIZE * 5, 0))

    # Desenha as letras
    for stream in _streams:
        x = stream["x"]
        for idx, y in enumerate(stream["letters"]):
            letter = random.choice(LETTERS)
            # Brilho no topo
            if idx == len(stream["letters"]) - 1:
                color = BRIGHT_COLOR
            else:
                color = TAIL_COLOR
            surf = font.render(letter, True, color)
            tela.blit(surf, (x, int(y)))
