import pygame as pg

ITENS_DISPONIVEIS_MERCADO = [
    'Pão', 'Carne', 'Maçã', 'Cenoura', 'Tomate', 'Cebola', 'Açúcar', 'Farinha',
    'Queijo', 'Manteiga', 'Leite', 'Fermento em pó', 'Chocolate', 'Ovo', 'Óleo']


class ListaCompras:
    def __init__(self, itens_necessarios):
        self.itens = itens_necessarios  # lista de strings
        self.visivel = False

    def alternar_visibilidade(self):
        self.visivel = not self.visivel

    def desenhar(self, tela):
        if not self.visivel:
            return

        pg.draw.rect(tela, (50, 50, 50), (600, 100, 300, 300))
        fonte = pg.font.SysFont("Arial", 24)

        for i, item in enumerate(self.itens):
            texto = fonte.render(f"- {item}", True, (255, 255, 255))
            tela.blit(texto, (620, 120 + i * 30))
