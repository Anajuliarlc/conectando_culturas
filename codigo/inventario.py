import pygame as pg

class Inventario:
    def __init__(self):
        self.itens = []
        self.visivel = False
        self.selecionado = 0

    def alternar_visibilidade(self):
        self.visivel = not self.visivel

    def navegar(self, direcao):
        if not self.itens:
            return
        self.selecionado = (self.selecionado + direcao) % len(self.itens)

    def adicionar_item(self, item):
        self.itens.append(item)

    def desenhar(self, tela):
        if not self.visivel:
            return

        # fundo do inventário
        pg.draw.rect(tela, (50, 50, 50), (100, 100, 400, 400))

        # desenha os itens
        fonte = pg.font.SysFont("Arial", 24)
        for i, item in enumerate(self.itens):
            cor = (255, 255, 0) if i == self.selecionado else (255, 255, 255)
            texto = fonte.render(item.nome_portugues, True, cor)
            tela.blit(texto, (120, 120 + i * 30))
