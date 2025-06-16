import pygame as pg
from config import *
from personagem import Personagem
from pytmx.util_pygame import load_pygame
import pytmx
import os

class Nivel_cidade:
    def __init__(self):
        self.colocar_superficie = pg.display.get_surface()
        self.tds_sprites = pg.sprite.Group()
        self.colisores = []

        caminho_mapa = os.path.join("niveis_data", "cmap_tilesets", "mapcid.tmx")
        self.tmx_data = load_pygame(caminho_mapa)

        largura = self.tmx_data.width * self.tmx_data.tilewidth
        altura = self.tmx_data.height * self.tmx_data.tileheight
        self.mapa_surface = pg.Surface((largura, altura))
        self.carregar_mapa()

        self.largura_mapa = largura
        self.altura_mapa = altura

        centro_mapa_x = largura // 2
        centro_mapa_y = altura // 2
        self.personagem = Personagem((centro_mapa_x, centro_mapa_y), self.tds_sprites)
        

    def carregar_mapa(self):
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    if gid != 0:
                        tile = self.tmx_data.get_tile_image_by_gid(gid)
                        if tile:
                            px = x * self.tmx_data.tilewidth
                            py = y * self.tmx_data.tileheight
                            self.mapa_surface.blit(tile, (px, py))

        for layer in self.tmx_data.layers:
            if isinstance(layer, pytmx.TiledObjectGroup):
                for obj in layer:
                    if obj.name == "colisor" or obj.type == "colisor":
                        self.colisores.append(pg.Rect(obj.x, obj.y, obj.width, obj.height))

    def rodar(self, dt):
        self.personagem.update(dt)

        # Verifica colisão após movimento
        for colisor in self.colisores:
            if self.personagem.hitbox.colliderect(colisor):
                self.personagem.cancelar_ultimo_movimento()
                break

        # Limpa a tela
        self.colocar_superficie.fill((0, 0, 0))

        # Desenha o mapa fixo
        self.colocar_superficie.blit(self.mapa_surface, (0, 0))

        # Desenha o personagem
        self.colocar_superficie.blit(self.personagem.image, self.personagem.rect)
        
