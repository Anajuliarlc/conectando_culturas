import pygame as pg
from config import *
from personagem import Personagem

class Nivel_cidade:
    def __init__(self):
        self.colocar_superficie = pg.display.get_surface()
        self.tds_sprites = pg.sprite.Group()
        self.setup()

    def setup(self):
        self.personagem = Personagem((640,360), self.tds_sprites)
                
    def rodar(self, dt):
        self.colocar_superficie.fill((52, 150, 77)) #60, 162, 112
        self.tds_sprites.update(dt)
        self.tds_sprites.draw(self.colocar_superficie)