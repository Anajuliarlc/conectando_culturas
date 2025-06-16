import pygame as pg
from config import *
from personagem import Personagem
from pytmx.util_pygame import load_pygame
import pytmx
import os

class BaseNivel:
    def __init__(self, caminho_mapa, nome_personagem, pos_inicial):
        self.colocar_superficie = pg.display.get_surface()
        self.tds_sprites = pg.sprite.Group()
        self.colisores = []
        self.transicoes = []  # Lista de transições (pg.Rect + destino)
        self.fonte = pg.font.SysFont("Arial", 24)
        self.tmx_data = load_pygame(caminho_mapa)

        largura = self.tmx_data.width * self.tmx_data.tilewidth
        altura = self.tmx_data.height * self.tmx_data.tileheight
        self.mapa_surface = pg.Surface((largura, altura))
        self.carregar_mapa()

        self.largura_mapa = largura
        self.altura_mapa = altura

        #centro_mapa_x = largura // 2
        #centro_mapa_y = altura // 2
        self.personagem = Personagem(pos_inicial, self.tds_sprites, nome_personagem)


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

                    if obj.name == "porta_mercado" or (obj.type == "transicao" and obj.name):
                        rect = pg.Rect(obj.x, obj.y, obj.width, obj.height)
                        self.transicoes.append({"rect": rect, "destino": obj.name})

    def rodar(self, dt):
        self.personagem.update(dt)

        for colisor in self.colisores:
            if self.personagem.hitbox.colliderect(colisor):
                self.personagem.cancelar_ultimo_movimento()
                break

        self.colocar_superficie.fill((0, 0, 0))
        self.colocar_superficie.blit(self.mapa_surface, (0, 0))
        self.colocar_superficie.blit(self.personagem.image, self.personagem.rect)

        self.transicao_ativa = None
        for t in self.transicoes:
            if self.personagem.hitbox.colliderect(t["rect"]):
                self.transicao_ativa = t["destino"]
                texto = self.fonte.render("Aperte ENTER para entrar", True, (0, 0, 0))
                self.colocar_superficie.blit(texto, (215, 180)) 
                break



class Nivel_cidade(BaseNivel):
    def __init__(self, nome_personagem):
        caminho_mapa = os.path.join("niveis_data", "cmap_tilesets", "mapcid.tmx")
        pos_inicial = (864, 704)
        super().__init__(caminho_mapa, nome_personagem, pos_inicial)

class Nivel_mercado(BaseNivel):
    def __init__(self, nome_personagem):
        caminho_mapa = os.path.join("niveis_data", "mmap_tilesets", "mapmerc.tmx")
        pos_inicial = (288, 704)
        super().__init__(caminho_mapa, nome_personagem, pos_inicial)