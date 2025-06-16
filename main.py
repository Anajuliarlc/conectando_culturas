import pygame as pg
import sys
import os
import random

sys.path.insert(0, "./codigo")

from config import *
from nivel import Nivel_cidade, Nivel_mercado
from inventario import Inventario
from tela_selecao import TelaSelecao
from menu_principal import MenuPrincipal
from tela_opcoes import TelaOpcoes
from gerenciador_sons import GerenciadorSons
from lista_compras import ListaCompras, ITENS_DISPONIVEIS_MERCADO
from quiz_final import QuizFinal
from tela_vitoria import TelaVitoria

class Jogo:
    def __init__(self):
        pg.init()
        self.tela = pg.display.set_mode((tela_comp, tela_alt))
        pg.display.set_caption('Conectando Culturas')
        self.relogio = pg.time.Clock()
        self.estado = 'menu'  # menu, selecao, cidade, mercado, quiz, vitoria, opcoes
        self.nome_personagem = 'pfem'  # padrão
        self.nivel = None
        self.som = GerenciadorSons()
        self.inventario = Inventario(self.som)
        self.menu = MenuPrincipal(self.som)
        self.selecao = TelaSelecao(self.som)
        self.opcoes = TelaOpcoes(self.som)
        itens_aleatorios = random.sample(ITENS_DISPONIVEIS_MERCADO, 4) 
        self.lista_compras = ListaCompras(itens_aleatorios)
        self.quiz = QuizFinal(self.som)
        self.vitoria = TelaVitoria(self.som)
        self.som.tocar_musica()

    def iniciar_nivel(self, nome_nivel):
        if nome_nivel == 'cidade':
            self.nivel = Nivel_cidade(self.nome_personagem, self.inventario, self.som)
        elif nome_nivel == 'mercado':
            self.nivel = Nivel_mercado(self.nome_personagem, self.inventario, self.lista_compras, self.som)
        self.inventario.set_nivel(self.nivel)

    def rodar(self):
        while True:
            dt = self.relogio.tick(60) / 1000
            teclas = pg.key.get_pressed()

            eventos = pg.event.get()  # captura todos os eventos uma vez

            for evento in eventos:
                if evento.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

                if evento.type == pg.KEYDOWN:
                    if evento.key == pg.K_ESCAPE:
                        pg.quit()
                        sys.exit()

                    # Controle inventário e lista compras no mapa
                    if self.estado in ['cidade', 'mercado']:
                        if evento.key == pg.K_i:
                            if self.estado == 'mercado':
                                self.inventario.alternar_visibilidade()
                        elif evento.key == pg.K_UP:
                            self.inventario.navegar(-1)
                        elif evento.key == pg.K_DOWN:
                            self.inventario.navegar(1)
                        elif evento.key == pg.K_r:
                            if self.inventario.visivel:
                                self.inventario.remover_item()
                        elif evento.key == pg.K_l:
                            if self.estado == 'mercado':
                                self.lista_compras.alternar_visibilidade()
                        elif evento.key == pg.K_o:
                            self.estado = 'opcoes'

                    elif self.estado == 'opcoes':
                        if evento.key == pg.K_o:
                            self.estado = 'cidade' if isinstance(self.nivel, Nivel_cidade) else 'mercado'

            # Agora, para cada estado, passo os eventos para o método rodar de cada tela

            if self.estado == 'menu':
                resultado = self.menu.rodar(eventos)
                if resultado == 'Jogar':
                    self.estado = 'selecao'
                elif resultado == 'Opções':
                    self.estado = 'opcoes'
                    self.som.tocar_click()
                elif resultado == 'Sair':
                    pg.quit()
                    sys.exit()

            elif self.estado == 'selecao':
                resultado = self.selecao.rodar(eventos)
                if resultado in ['pmasc', 'pfem']:
                    self.nome_personagem = resultado
                    self.estado = 'cidade'
                    self.iniciar_nivel('cidade')
                    self.som.tocar_click()

            elif self.estado == 'opcoes':
                resultado = self.opcoes.rodar(eventos)
                self.som.atualizar_volumes(self.opcoes.volume_musica, self.opcoes.volume_sfx)
                if resultado:  # somente se tela opcoes sinalizar para sair dela
                    if self.nivel is not None:
                        self.estado = 'cidade' if isinstance(self.nivel, Nivel_cidade) else 'mercado'
                    else:
                        self.estado = 'menu'

            elif self.estado in ['cidade', 'mercado']:
                self.nivel.rodar(dt, teclas, eventos)
                if hasattr(self.nivel, "estado_quiz") and self.nivel.estado_quiz:
                    self.estado = "quiz"

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
                self.lista_compras.desenhar(self.tela)

            elif self.estado == 'quiz':
                resultado = self.quiz.rodar(eventos)
                if resultado == 'vitoria':
                    self.estado = 'vitoria'
                    self.som.parar_musica()
                    self.som.tocar_musica_vitoria()
                elif resultado == 'falha':
                    self.estado = 'mercado'
                    self.iniciar_nivel('mercado')
                    self.quiz = QuizFinal(self.som)

            elif self.estado == 'vitoria':
                resultado = self.vitoria.rodar(eventos)
                if resultado == 'menu':
                    self.estado = 'menu'
                    self.som.tocar_musica()
                elif resultado == 'sair':
                    pg.quit()
                    sys.exit()

            #pg.display.flip()
            pg.display.update()
            self.relogio.tick(60)
            


if __name__ == '__main__':
    jogo = Jogo()
    jogo.rodar()
