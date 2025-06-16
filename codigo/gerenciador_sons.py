import pygame as pg
import os

class GerenciadorSons:
    def __init__(self):
        self.sons = {}
        self.volume_musica = 0.5
        self.volume_sfx = 0.5

        caminho = os.path.join("niveis_data", "sons")
        self.sons["click"] = pg.mixer.Sound(os.path.join(caminho, "clicksom.mp3"))
        self.sons["click"].set_volume(self.volume_sfx)

        self.musica_path = os.path.join(caminho, "fundo_jogo.mp3")
        pg.mixer.music.load(self.musica_path)
        pg.mixer.music.set_volume(self.volume_musica)

    def tocar_click(self):
        self.sons["click"].play()

    def tocar_musica(self):
        pg.mixer.music.play(-1)

    def ajustar_volume_musica(self, delta):
        self.volume_musica = min(1.0, max(0.0, self.volume_musica + delta))
        pg.mixer.music.set_volume(self.volume_musica)

    def ajustar_volume_sfx(self, delta):
        self.volume_sfx = min(1.0, max(0.0, self.volume_sfx + delta))
        self.sons["click"].set_volume(self.volume_sfx)
        self.tocar_click()

    def atualizar_volumes(self, novo_volume_musica, novo_volume_sfx):
        self.volume_musica = novo_volume_musica
        self.volume_sfx = novo_volume_sfx
        pg.mixer.music.set_volume(self.volume_musica)
        self.sons["click"].set_volume(self.volume_sfx)