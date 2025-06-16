import pygame as pg
from config import *

class TelaVitoria:
    def __init__(self, som):
        self.som = som
        self.opcoes = ["Voltar ao menu", "Sair do jogo"]
        self.selecionado = 0
        self.fonte = pg.font.SysFont("Arial", 32)
        self.fonte_grande = pg.font.SysFont("Arial", 48, bold=True)
        self.relogio = pg.time.Clock()

    def atualizar(self, eventos):
        for evento in eventos:
            if evento.type == pg.KEYDOWN:
                if evento.key == pg.K_w:
                    self.selecionado = (self.selecionado - 1) % len(self.opcoes)
                    self.som.tocar_click()
                elif evento.key == pg.K_s:
                    self.selecionado = (self.selecionado + 1) % len(self.opcoes)
                    self.som.tocar_click()
                elif evento.key == pg.K_RETURN:
                    self.som.tocar_click()
                    if self.selecionado == 0:
                        return 'menu'  # Voltar ao menu
                    else:
                        return 'sair'  # Sair do jogo
        return None

    def desenhar(self, tela):
        tela.fill((0, 0, 0))

        # Mensagem de vitória
        mensagem = "Parabéns! Você completou a missão!"
        texto_msg = self.fonte_grande.render(mensagem, True, (255, 255, 255))
        rect_msg = texto_msg.get_rect(center=(tela_comp // 2, 100))
        tela.blit(texto_msg, rect_msg)

        # Botões
        for i, opcao in enumerate(self.opcoes):
            cor = (255, 255, 255) if i == self.selecionado else (255, 230, 0)
            texto = self.fonte.render(opcao, True, cor)
            rect = texto.get_rect(center=(tela_comp // 2, 250 + i * 60))
            tela.blit(texto, rect)

    def rodar(self, eventos):
        resultado = self.atualizar(eventos)
        self.desenhar(pg.display.get_surface())
        pg.display.flip()
        self.relogio.tick(60)
        return resultado

