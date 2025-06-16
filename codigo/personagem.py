import pygame as pg
from config import *
from lista_controles import ListaControles
import os

def carregar_sprites_personagem(nome):
    cam_base = os.path.join("niveis_data", "personagens_img")
    tamanho = (200, 350)
    return {
        'cima': pg.transform.scale(pg.image.load(os.path.join(cam_base, f"{nome}_w.png")).convert_alpha(), tamanho),
        'baixo': pg.transform.scale(pg.image.load(os.path.join(cam_base, f"{nome}_s.png")).convert_alpha(), tamanho),
        'esquerda': pg.transform.scale(pg.image.load(os.path.join(cam_base, f"{nome}_a.png")).convert_alpha(), tamanho),
        'direita': pg.transform.scale(pg.image.load(os.path.join(cam_base, f"{nome}_d.png")).convert_alpha(), tamanho)
    }

class Personagem(pg.sprite.Sprite):
    def __init__(self, pos, grupo, nome_personagem):

        super().__init__(grupo)

        self.sprites = carregar_sprites_personagem(nome_personagem)
        self.direcao_atual = 'baixo'
        self.image = self.sprites[self.direcao_atual]
        self.rect = self.image.get_rect(midbottom = pos)
        self.hitbox = pg.Rect(0, 0, 30, 50)  # menor que o sprite
        offset_y = 40 # ← tente ajustar entre 30-50 conforme o visual do sprite
        self.hitbox.midbottom = (self.rect.centerx, self.rect.bottom - offset_y)

        self.direction = pg.math.Vector2()
        self.pos = pg.math.Vector2(self.rect.midbottom)
        self.pos_anterior = self.pos.copy()
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
        self.pos_anterior = self.pos.copy()
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
        self.pos.y += self.direction.y * self.speed * dt
        self.hitbox.midbottom = (round(self.pos.x), round(self.pos.y))
        self.rect.midbottom = self.hitbox.midbottom


        #self.pos.y += self.direction.y * self.speed * dt
        #self.hitbox.centery = round(self.pos.y)
        #self.rect.centery = self.hitbox.centery

    def update(self, dt):
        self.input()
        self.mover(dt)

    def cancelar_ultimo_movimento(self):
        self.pos = self.pos_anterior.copy()
        #self.hitbox.center = self.pos
        #self.rect.midbottom = self.hitbox.midbottom
        self.hitbox.midbottom = self.pos
        self.rect.midbottom = self.hitbox.midbottom