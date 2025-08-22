import pygame
import sys
import io

# Importa constantes e funções utilitárias
from utils import LARGURA, ALTURA, FPS

# Importa todas as cenas
import cena1, cena2, cena3, cena4, cena5

# Garante saída UTF-8 no console
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def main():
    """Função principal que inicializa o Pygame, gerencia eventos e troca de cenas."""
    pygame.init()
    
    # Configura a tela inicial como redimensionável
    tela = pygame.display.set_mode((LARGURA, ALTURA), pygame.RESIZABLE)
    pygame.display.set_caption("Controle de Cor com Cenas")
    
    clock = pygame.time.Clock()
    cena_atual = 1  # Cena inicial
    
    # Inicializa a cena 1 com o centro correto
    w, h = tela.get_size()
    if hasattr(cena1, "init_scene"):
        cena1.init_scene(w, h)

    executando = True
    while executando:
        for evento in pygame.event.get():
            # Evento de saída
            if evento.type == pygame.QUIT:
                executando = False

            # Evento de redimensionamento da janela
            elif evento.type == pygame.VIDEORESIZE:
                tela = pygame.display.set_mode((evento.w, evento.h), pygame.RESIZABLE)
                # Atualiza centros de cenas que dependem do tamanho
                if cena_atual == 1 and hasattr(cena1, "init_scene"):
                    cena1.init_scene(evento.w, evento.h)
                elif cena_atual == 5 and hasattr(cena5, "init_scene"):
                    cena5.init_scene(evento.w, evento.h)

            # Evento de pressionamento de teclas para troca de cenas
            elif evento.type == pygame.KEYDOWN:
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
                elif evento.key == pygame.K_F5:
                    cena_atual = 5
                    print("[Cena 5] Ativada")

            # Encaminha eventos para a cena ativa (se existir a função handle_event)
            if cena_atual == 1 and hasattr(cena1, "handle_event"):
                cena1.handle_event(evento, tela)
            elif cena_atual == 2 and hasattr(cena2, "handle_event"):
                cena2.handle_event(evento)
            elif cena_atual == 3 and hasattr(cena3, "handle_event"):
                cena3.handle_event(evento)
            elif cena_atual == 4 and hasattr(cena4, "handle_event"):
                cena4.handle_event(evento)
            elif cena_atual == 5 and hasattr(cena5, "handle_event"):
                cena5.handle_event(evento, tela)

        # Renderiza a cena ativa
        if cena_atual == 1:
            cena1.update_and_draw(tela)
        elif cena_atual == 2:
            cena2.cena2(tela)
        elif cena_atual == 3:
            cena3.cena3(tela)
        elif cena_atual == 4:
            cena4.cena4(tela)
        elif cena_atual == 5:
            cena5.update_and_draw(tela)  

        # Atualiza a tela e mantém FPS constante
        pygame.display.flip()
        clock.tick(FPS)

    # Finaliza Pygame e sai do programa
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
