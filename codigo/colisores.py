import pygame as pg

class Colisor(pg.sprite.Sprite):
    """Sprite invisível que bloqueia o personagem"""
    def __init__(self, pos, size, grupo):
        super().__init__(grupo)
        self.image = pg.Surface(size)
        self.image.set_alpha(0)          # invisível
        self.rect = self.image.get_rect(topleft=pos)