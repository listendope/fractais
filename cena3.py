import pygame

def cena3(tela):
    largura, altura = tela.get_size()
    tela.fill((20, 20, 20))
    fonte = pygame.font.SysFont(None, 60)
    sub = pygame.font.SysFont(None, 28)
    texto = fonte.render("Cena 3 - Em desenvolvimento", True, (250, 250, 250))
    dica = sub.render("Use 1/2/3 para alternar cenas", True, (190, 190, 190))
    tela.blit(texto, (max(20, largura // 2 - texto.get_width() // 2), altura // 2 - 40))
    tela.blit(dica, (max(20, largura // 2 - dica.get_width() // 2), altura // 2 + 20))
