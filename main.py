import pygame
import sys
from utils import LARGURA, ALTURA, FPS
import cena1
import cena2
import cena3

def main():
    pygame.init()
    tela = pygame.display.set_mode((LARGURA, ALTURA), pygame.RESIZABLE)
    pygame.display.set_caption("Controle de Cor com Cenas")
    clock = pygame.time.Clock()

    cena_atual = 1
    # Inicializa a cena 1 com o centro correto
    w, h = tela.get_size()
    if hasattr(cena1, "init_scene"):
        cena1.init_scene(w, h)

    executando = True
    while executando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                executando = False

            elif evento.type == pygame.VIDEORESIZE:
                # Recria a tela com o novo tamanho
                tela = pygame.display.set_mode((evento.w, evento.h), pygame.RESIZABLE)
                # Atualiza centro da cena 1 quando a janela for redimensionada
                if cena_atual == 1 and hasattr(cena1, "init_scene"):
                    cena1.init_scene(evento.w, evento.h)

            elif evento.type == pygame.KEYDOWN:
                # Troca de cenas (global)
                if evento.key == pygame.K_1:
                    cena_atual = 1
                elif evento.key == pygame.K_2:
                    cena_atual = 2
                elif evento.key == pygame.K_3:
                    cena_atual = 3

            # Encaminha eventos para a cena ativa
            if cena_atual == 1 and hasattr(cena1, "handle_event"):
                cena1.handle_event(evento, tela)
            elif cena_atual == 2 and hasattr(cena2, "handle_event"):
                cena2.handle_event(evento)
            # Cena 3 não tem controles extras no momento

        # Render da cena ativa
        if cena_atual == 1:
            cena1.update_and_draw(tela)
        elif cena_atual == 2:
            cena2.cena2(tela)
        elif cena_atual == 3:
            cena3.cena3(tela)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
