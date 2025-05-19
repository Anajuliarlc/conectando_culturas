import pygame as pg
from config import *
from lista_controles import ListaControles
import os

def carregar_sprites_personagem():
    cam_base = os.path.join("niveis_data", "personagens_img")
    tamanho = (300, 450)  # largura x altura ideal
    return {
        'cima': pg.transform.scale(pg.image.load(os.path.join(cam_base, "pmasc_w.png")).convert_alpha(), tamanho),
        'baixo': pg.transform.scale(pg.image.load(os.path.join(cam_base, "pmasc_s.png")).convert_alpha(), tamanho),
        'esquerda': pg.transform.scale(pg.image.load(os.path.join(cam_base, "pmasc_a.png")).convert_alpha(), tamanho),
        'direita': pg.transform.scale(pg.image.load(os.path.join(cam_base, "pmasc_d.png")).convert_alpha(), tamanho)
    }

class Personagem(pg.sprite.Sprite):
    def __init__(self, pos, grupo):

        super().__init__(grupo)

        self.sprites = carregar_sprites_personagem()
        self.direcao_atual = 'baixo'
        self.image = self.sprites[self.direcao_atual]
        self.rect = self.image.get_rect(center = pos) 

        self.direction = pg.math.Vector2()
        self.pos = pg.math.Vector2(self.rect.center)
        self.speed = 200

    
    def input(self):
        keys = pg.key.get_pressed()
        mudou_direcao = False

        # vertical
        if keys[ListaControles.cima.value]:
            self.direction.y = -1
            self.direcao_atual = 'cima'
            mudou_direcao = True
        elif keys[ListaControles.baixo.value]:
            self.direction.y = 1
            self.direcao_atual = 'baixo'
            mudou_direcao = True
        else:
            self.direction.y = 0

        # horizontal
        if keys[ListaControles.direita.value]:
            self.direction.x = 1
            self.direcao_atual = 'direita'
            mudou_direcao = True
        elif keys[ListaControles.esquerda.value]:
            self.direction.x = -1
            self.direcao_atual = 'esquerda'
            mudou_direcao = True
        else:
            self.direction.x = 0

        if mudou_direcao:
            self.image = self.sprites[self.direcao_atual]

    def mover(self, dt):
        # Se houver alguma direção pressionada, normaliza o vetor.
        # Isso é necessário para evitar que o personagem se mova mais rápido na diagonal.
        # Exemplo: se o jogador pressionar 'W' e 'D' ao mesmo tempo (cima + direita),
        # Se a direção for (1, 1), a magnitude é √(1² + 1²) = √2 ≈ 1.41, (conceito de pitagoras)
        # o que causaria um deslocamento 41% mais rápido sem normalização.
        # O método normalize() ajusta o vetor para manter a mesma direção,
        #O vetor vira (0.71, 0.71), mantendo o módulo 1
        # e evitando vantagem de velocidade em diagonais.
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        #controle separado p/ melhorar colisões
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.centerx = self.pos.x

        self.pos.y += self.direction.y * self.speed * dt
        self.rect.centery = self.pos.y

    def update(self, dt):
        self.input()
        self.mover(dt)