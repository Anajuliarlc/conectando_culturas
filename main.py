import pygame as pg, sys
sys.path.insert(0, "./codigo")
from config import *
from nivel import Nivel_cidade

class Jogo:
    def __init__(self):
        pg.init()
        self.tela = pg.display.set_mode((tela_comp, tela_alt))
        titulo = pg.display.set_caption('Conectando Culturas')
        self.relogio = pg.time.Clock()
        self.nivel_cid = Nivel_cidade()

    def rodar(self):
        while True:
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

            #dt = delta time - tempo decorrido
            dt = self.relogio.tick() / 1000 
            self.nivel_cid.rodar(dt)
            pg.display.update()


if __name__ == '__main__':
    jogo = Jogo()
    jogo.rodar()