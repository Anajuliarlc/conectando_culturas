import pygame as pg
import sys
sys.path.insert(0, "./codigo")
from config import *
from nivel import Nivel_cidade

class Jogo:
    def __init__(self):
        pg.init()
        self.tela = pg.display.set_mode((tela_comp, tela_alt))
        pg.display.set_caption('Conectando Culturas')
        self.relogio = pg.time.Clock()
        self.nivel_cid = Nivel_cidade()

    def rodar(self):
        while True:
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

            dt = self.relogio.tick(60) / 1000  # Limita a 60 FPS e calcula delta time
            self.nivel_cid.rodar(dt)
            pg.display.update()

if __name__ == '__main__':
    jogo = Jogo()
    jogo.rodar()