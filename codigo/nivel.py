import pygame as pg
from config import *
from personagem import Personagem
from pytmx.util_pygame import load_pygame
import pytmx
import os

class BaseNivel:
    def __init__(self, caminho_mapa, nome_personagem, pos_inicial, inventario):
        self.colocar_superficie = pg.display.get_surface()
        self.tds_sprites = pg.sprite.Group()
        self.colisores = []
        self.transicoes = []
        self.transicao_ativa = None
        self.fonte = pg.font.SysFont("Arial", 24)
        self.tmx_data = load_pygame(caminho_mapa)
        self.itens_mapa = []
        self.item_proximo = None
        self.inventario = inventario

        largura = self.tmx_data.width * self.tmx_data.tilewidth
        altura = self.tmx_data.height * self.tmx_data.tileheight
        self.mapa_surface = pg.Surface((largura, altura))
        self.carregar_mapa()

        self.largura_mapa = largura
        self.altura_mapa = altura

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

                    elif obj.name and obj.name.startswith("porta_"):
                        rect = pg.Rect(obj.x, obj.y, obj.width, obj.height)
                        destino = obj.name.split("porta_")[1]
                        self.transicoes.append({"rect": rect, "destino": destino})

                    elif obj.name and obj.name.startswith("item_") and "nome_portugues" in obj.properties and "nome_ingles" in obj.properties:
                        self.itens_mapa.append({
                            "rect": pg.Rect(obj.x, obj.y, obj.width, obj.height),
                            "nome_portugues": obj.properties["nome_portugues"],
                            "nome_ingles": obj.properties["nome_ingles"]
                        })

        self.itens_originais = [item.copy() for item in self.itens_mapa]
        
    def recolocar_item_no_mapa(self, item):
        # Adiciona o item na lista dos itens do mapa para reaparecer
        self.itens_mapa.append(item)

    def rodar(self, dt, teclas):
        self.personagem.update(dt)

        for colisor in self.colisores:
            if self.personagem.hitbox.colliderect(colisor):
                self.personagem.cancelar_ultimo_movimento()
                break

        self.transicao_ativa = None
        for t in self.transicoes:
            if self.personagem.hitbox.colliderect(t["rect"]):
                self.transicao_ativa = t["destino"]
                break

        # Detectar item próximo
        self.item_proximo = None
        for item in self.itens_mapa:
            if self.personagem.hitbox.colliderect(item["rect"]):
                self.item_proximo = item
                break

        # Se pressionou Enter e tem item próximo, adicionar ao inventário
        if self.item_proximo and teclas[pg.K_RETURN]:
            self.inventario.adicionar_item(self.item_proximo)
            self.itens_mapa.remove(self.item_proximo)
            self.item_proximo = None

        # Renderização
        self.colocar_superficie.fill((0, 0, 0))
        self.colocar_superficie.blit(self.mapa_surface, (0, 0))
        self.colocar_superficie.blit(self.personagem.image, self.personagem.rect)

        # Mostrar dica de transição
        if self.transicao_ativa:
            texto = self.fonte.render("Aperte ENTER para entrar", True, (0, 0, 0))
            self.colocar_superficie.blit(texto, (215, 290))

        # Mostrar nome do item
        for item in self.itens_mapa:
            nome_portugues = item["nome_portugues"]
            nome_ingles = item["nome_ingles"]

            texto_pt = self.fonte.render(nome_portugues, True, (0, 0, 0))
            texto_en = self.fonte.render(nome_ingles, True, (0, 0, 0))

            x = item["rect"].centerx
            y = item["rect"].top - 20  # posição da primeira linha

            self.colocar_superficie.blit(texto_pt, texto_pt.get_rect(center=(x, y)))
            self.colocar_superficie.blit(texto_en, texto_en.get_rect(center=(x, y + 20)))  # linha de baixo

class Nivel_cidade(BaseNivel):  
    def __init__(self, nome_personagem, inventario):  
        caminho_mapa = os.path.join("niveis_data", "cmap_tilesets", "mapcid.tmx")  
        pos_inicial = (864, 704)  
        super().__init__(caminho_mapa, nome_personagem, pos_inicial, inventario)  

class Nivel_mercado(BaseNivel):  
    def __init__(self, nome_personagem, inventario):  
        caminho_mapa = os.path.join("niveis_data", "mmap_tilesets", "mapmerc.tmx")  
        pos_inicial = (288, 704)  
        super().__init__(caminho_mapa, nome_personagem, pos_inicial, inventario)  
