import pygame as pg
import os
from config import *
from gerenciador_sons import GerenciadorSons

class MenuPrincipal:
    def __init__(self, gerenciador_sons):
        self.tela = pg.display.get_surface()
        self.relogio = pg.time.Clock()
        self.fonte = pg.font.SysFont("Arial", 64, bold=True)
        self.opcoes = ["Jogar", "Opções", "Sair"]
        self.index = 0
        self.sons = gerenciador_sons

        self.imagem_canto_fem = pg.image.load(os.path.join("niveis_data", "personagens_img", "pfem_inicio.png")).convert_alpha()
        self.imagem_canto_fem = pg.transform.scale(self.imagem_canto_fem, (400, 400))

        self.imagem_canto_masc = pg.image.load(os.path.join("niveis_data", "personagens_img", "pmasc_inicio.png")).convert_alpha()
        self.imagem_canto_masc = pg.transform.scale(self.imagem_canto_masc, (400, 400))

    def desenhar(self):
        self.tela.fill((0, 0, 0))  # Fundo preto

        titulo = self.fonte.render("Conectando Culturas", True, (255, 255, 255))
        self.tela.blit(titulo, titulo.get_rect(center=(672, 100)))

        for i, texto in enumerate(self.opcoes):
            cor_caixa = (255, 255, 255) if i == self.index else (255, 230, 0)
            texto_cor = (0, 0, 0)

            rend = self.fonte.render(texto, True, texto_cor)
            rect = rend.get_rect(center=(672, 250 + i * 100))

            pg.draw.rect(self.tela, cor_caixa, rect.inflate(40, 20), border_radius=10)
            self.tela.blit(rend, rect)

        rect = self.imagem_canto_fem.get_rect()
        margem = 20  # distância da borda
        rect.bottomright = (tela_comp - margem, tela_alt - margem)
        self.tela.blit(self.imagem_canto_fem, rect)

        rect_masc = self.imagem_canto_masc.get_rect()
        rect_masc.bottomleft = (margem, tela_alt - margem)
        self.tela.blit(self.imagem_canto_masc, rect_masc)

    def rodar(self, eventos):
        for e in eventos:
            if e.type == pg.QUIT:
                self.sons.tocar_click()
                pg.quit()
                exit()
            elif e.type == pg.KEYDOWN:
                if e.key == pg.K_w:
                    self.index = (self.index - 1) % len(self.opcoes)
                    self.sons.tocar_click()
                elif e.key == pg.K_s:
                    self.index = (self.index + 1) % len(self.opcoes)
                    self.sons.tocar_click()
                elif e.key == pg.K_RETURN:
                    self.sons.tocar_click()
                    return self.opcoes[self.index]

        self.desenhar()
        pg.display.flip()
        self.relogio.tick(60)
        return None

