import pygame as pg
from enum import Enum

class ListaControles(Enum):
    """Enumeração de controles do jogo"""
    cima = pg.K_w
    baixo = pg.K_s
    esquerda = pg.K_a
    direita = pg.K_d
    espaco = pg.K_SPACE
    esc = pg.K_ESCAPE
    enter = pg.K_RETURN
    inventario = pg.K_i
    opcoes = pg.K_o
    sair = pg.QUIT