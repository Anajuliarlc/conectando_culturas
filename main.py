import pygame as pg
import sys
sys.path.insert(0, "./codigo")
from config import *
from nivel import Nivel_cidade, Nivel_mercado
from tela_selecao import TelaSelecao  # ← importa a nova tela

class Jogo:
    def __init__(self):
        pg.init()
        self.tela = pg.display.set_mode((tela_comp, tela_alt))
        pg.display.set_caption('Conectando Culturas')
        self.relogio = pg.time.Clock()

        # Inicia a tela de seleção de personagem
        selecao = TelaSelecao()
        self.nome_personagem = selecao.rodar()  # ← guarda o personagem escolhido

        self.nivel = Nivel_cidade(self.nome_personagem)

    def trocar_nivel(self, nome_destino):
        if nome_destino == "mercado":
            self.nivel = Nivel_mercado(self.nome_personagem)
        elif nome_destino == "cidade":
            self.nivel = Nivel_cidade(self.nome_personagem)

    def rodar(self):
        while True:
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if evento.type == pg.KEYDOWN:
                    if evento.key == pg.K_RETURN and hasattr(self.nivel, 'transicao_ativa') and self.nivel.transicao_ativa:
                        self.trocar_nivel(self.nivel.transicao_ativa)

            dt = self.relogio.tick(60) / 1000
            self.nivel.rodar(dt)
            pg.display.update()

if __name__ == '__main__':
    jogo = Jogo()
    jogo.rodar()
