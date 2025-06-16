import pygame as pg

class Inventario:
    def __init__(self, som=None):
        self.itens = []
        self.visivel = False
        self.selecionado = 0
        self.nivel = None
        self.som = som

    def set_nivel(self, nivel):
        self.nivel = nivel

    def alternar_visibilidade(self):
        self.visivel = not self.visivel

    def navegar(self, direcao):
        if not self.itens:
            return
        self.selecionado = (self.selecionado + direcao) % len(self.itens)

    def adicionar_item(self, item):
        self.itens.append(item)
        if self.som:
            self.som.tocar_som_pegar_obj()

    def remover_item(self):
        if not self.itens:
            return
        item = self.itens.pop(self.selecionado)
        if self.selecionado >= len(self.itens):
            self.selecionado = len(self.itens) - 1

        # Se tem nível e método para recolocar o item
        if self.nivel:
            self.nivel.recolocar_item_no_mapa(item)


    def desenhar(self, tela):
        if not self.visivel:
            return

        # fundo do inventário
        pg.draw.rect(tela, (50, 50, 50), (100, 100, 400, 400))

        # desenha os itens
        fonte = pg.font.SysFont("Arial", 24)
        for i, item in enumerate(self.itens):
            cor = (255, 255, 0) if i == self.selecionado else (255, 255, 255)
            texto = fonte.render(item['nome_portugues'], True, cor)
            tela.blit(texto, (120, 120 + i * 30))
