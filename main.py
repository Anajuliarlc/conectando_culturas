import pygame as pg
import sys
import os

sys.path.insert(0, "./codigo")

from config import *
from nivel import Nivel_cidade, Nivel_mercado
from inventario import Inventario
from tela_selecao import TelaSelecao
from menu_principal import MenuPrincipal
from tela_opcoes import TelaOpcoes
from gerenciador_sons import GerenciadorSons

class Jogo:
    def __init__(self):
        pg.init()
        self.tela = pg.display.set_mode((tela_comp, tela_alt))
        pg.display.set_caption('Conectando Culturas')
        self.relogio = pg.time.Clock()
        self.estado = 'menu'  # menu, selecao, cidade, mercado, opcoes
        self.nome_personagem = 'pfem'  # padrão
        self.inventario = Inventario()
        self.nivel = None
        self.som = GerenciadorSons()  # <-- Cria o gerenciador de som primeiro
        self.menu = MenuPrincipal(self.som)  # <-- Agora pode passar
        self.selecao = TelaSelecao(self.som)
        self.opcoes = TelaOpcoes(self.som)
        self.som.tocar_musica()

    def iniciar_nivel(self, nome_nivel):
        if nome_nivel == 'cidade':
            self.nivel = Nivel_cidade(self.nome_personagem, self.inventario)
        elif nome_nivel == 'mercado':
            self.nivel = Nivel_mercado(self.nome_personagem, self.inventario)

    def rodar(self):
        while True:
            dt = self.relogio.tick(60) / 1000
            teclas = pg.key.get_pressed()

            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

                if evento.type == pg.KEYDOWN:
                    if evento.key == pg.K_ESCAPE:
                        pg.quit()
                        sys.exit()

                    if self.estado in ['cidade', 'mercado']:
                        if evento.key == pg.K_i:
                            if self.estado == 'mercado':  # só no mercado
                                self.inventario.alternar_visibilidade()
                        elif evento.key == pg.K_UP:
                            self.inventario.navegar(-1)
                        elif evento.key == pg.K_DOWN:
                            self.inventario.navegar(1)
                        elif evento.key == pg.K_r:
                            if self.inventario.visivel:
                                self.inventario.remover_selecionado()
                        elif evento.key == pg.K_o:
                            self.estado = 'opcoes'

                    elif self.estado == 'opcoes':
                        if evento.key == pg.K_o:
                            self.estado = 'cidade' if isinstance(self.nivel, Nivel_cidade) else 'mercado'


            if self.estado == 'menu':
                resultado = self.menu.rodar()
                if resultado == 'Jogar':
                    self.estado = 'selecao'
                elif resultado == 'Opções':
                    self.estado = 'opcoes'
                    self.som.tocar_click()
                elif resultado == 'Sair':
                    pg.quit()
                    sys.exit()

            elif self.estado == 'selecao':
                resultado = self.selecao.rodar()
                if resultado in ['pmasc', 'pfem']:
                    self.nome_personagem = resultado
                    self.estado = 'cidade'
                    self.iniciar_nivel('cidade')
                    self.som.tocar_click()

            elif self.estado == 'opcoes':
                resultado = self.opcoes.rodar()
                self.som.atualizar_volumes(self.opcoes.volume_musica, self.opcoes.volume_sfx)
                if self.nivel is not None:
                    self.estado = 'cidade' if isinstance(self.nivel, Nivel_cidade) else 'mercado'
                else:
                    self.estado = 'menu'

            elif self.estado in ['cidade', 'mercado']:
                self.nivel.rodar(dt, teclas)

                # Transição de mapas
                if self.nivel.transicao_ativa and teclas[pg.K_RETURN]:
                    destino = self.nivel.transicao_ativa
                    self.som.tocar_click()
                    if destino == 'mercado':
                        self.estado = 'mercado'
                        self.iniciar_nivel('mercado')
                    elif destino == 'cidade':
                        self.estado = 'cidade'
                        self.iniciar_nivel('cidade')

                self.inventario.desenhar(self.tela)

            pg.display.update()


if __name__ == '__main__':
    jogo = Jogo()
    jogo.rodar()
