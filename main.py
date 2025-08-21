import pygame
import sys
from utils import LARGURA, ALTURA, FPS
import cena1
import cena2
import cena3
import cena4


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
                if evento.key == pygame.K_F1:
                    cena_atual = 1
                    print("[Cena 1] Ativada")
                elif evento.key == pygame.K_F2:
                    cena_atual = 2
                    print("[Cena 2] Ativada")
                elif evento.key == pygame.K_F3:
                    cena_atual = 3
                    print("[Cena 3] Ativada")
                elif evento.key == pygame.K_F4:
                    cena_atual = 4
                    print("[Cena 4] Ativada")

            # Encaminha eventos para a cena ativa
            if cena_atual == 1 and hasattr(cena1, "handle_event"):
                cena1.handle_event(evento, tela)
            elif cena_atual == 2 and hasattr(cena2, "handle_event"):
                cena2.handle_event(evento)
            elif cena_atual == 3 and hasattr(cena3, "handle_event"):
                cena3.handle_event(evento)
            elif cena_atual == 4 and hasattr(cena4, "handle_event"):
                cena4.handle_event(evento)


        # Render da cena ativa
        if cena_atual == 1:
            cena1.update_and_draw(tela)
        elif cena_atual == 2:
            cena2.cena2(tela)
        elif cena_atual == 3:
            cena3.cena3(tela)
        elif cena_atual == 4:
            cena4.cena4(tela)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
