import pygame as pg
from abc import ABC, abstractmethod

class Tela(ABC):
    """Objeto abstrato de uma tela do jogo"""

    def __init__(self, titulo, icone): 
        """ Inicia o objeto abstrato da tela do jogo

        :param titulo: Título da tela
        :type titulo: str
        :param icone: Caminho de acesso do ícone da tela em png
        :type icone: str
        """             
        self.titulo = titulo
        self.icone = icone
        #32 é o tamanho padrão de um tile e temos 24 tiles na tela
        self.altura = 768
        self.largura = 1280
        self.fps = 30

    @abstractmethod
    def controles(self):
        """Verifica os inputs do usuário e define os controles dessa tela""" 
        pass

    @abstractmethod
    def iniciar(self, volume_musica, volume_sfx):
        """Inicia a tela"""
        pass