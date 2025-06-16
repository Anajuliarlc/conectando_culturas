import pygame as pg
import random
from config import *
from gerenciador_sons import GerenciadorSons

class QuizFinal:
    def __init__(self, gerenciador_sons):
        self.som = gerenciador_sons
        self.fonte = pg.font.Font(None, 48)  # Opções (antes 32)
        self.fonte_grande = pg.font.Font(None, 60)  # Perguntas (antes 48)
        self.fonte_contador = pg.font.Font(None, 54)  # Contador de acertos/erros
        self.reiniciar()

    def reiniciar(self):
        self.perguntas = self.carregar_perguntas()
        self.perguntas_atuais = random.sample(self.perguntas, 5)
        self.pergunta_atual = 0
        self.opcao_selecionada = 0
        self.acertos = 0
        self.erros = 0
        self.concluido = False
        self.resultado = None
        self.tempo_fim = 0

    def carregar_perguntas(self):
               return [
            {"pergunta": "Which fruit has the letter A in the market?",
                "opcoes": ["a) pear ", "b) banana", "c) apple", "d) grape"],
                "correta": 2},
            {"pergunta": "Which of these fruits was in the market?",
                "opcoes": ["a) pear ", "b) banana", "c) tomato", "d) grape"],
                "correta": 2},
            {"pergunta": "What is 'cenoura' in English?",
                "opcoes": ["a) lettuce", "b) carrot", "c) onion", "d) potato"],
                "correta": 1},
            {"pergunta": "What is 'farinha' in English?",
                "opcoes": ["a) flour", "b) sugar", "c) yeast", "d) rice"],
                "correta": 0},
            {"pergunta": "Which of these is dairy?",
                "opcoes": ["a) manteiga", "b) maçã", "c) chocolate", "d) tomate"],
                "correta": 0},
            {"pergunta": "Which of these is used to bake a cake?",
                "opcoes": ["a) Óleo", "b) Fermento em pó", "c) Farinha", "d) all of the above"],
                "correta": 3},
            {"pergunta": "Which of these is not found in the market?",
                "opcoes": ["a) rice", "b) chocolate", "c) egg", "d) butter"],
                "correta": 0},
            {"pergunta": "Which is the main ingredient to make a carrot cake?",
                "opcoes": ["a) cenoura ", "b) banana", "c) maçã", "d) flour"],
                "correta": 0},
            {"pergunta": "What is maçã?",
                "opcoes": ["a) pear ", "b) banana", "c) apple", "d) grape"],
                "correta": 2},
            {"pergunta": "What is açúcar for?",
                "opcoes": ["a) put in coffee ", "b) put in rice", "c) put in the egg", "d) put in cheese"],
                "correta": 0},
            {"pergunta": "Which is the translation of onion?",
                "opcoes": ["a) cebola ", "b) queijo", "c) arroz", "d) farinha"],
                "correta": 0},
            {"pergunta": "What do you buy at the butcher’s?",
                "opcoes": ["a) carne", "b) ovos", "c) Pão", "d) fermento em pó"],
                "correta": 0},
            {"pergunta": "Which ingredientes do I use to make pancake(panqueca)?",
                "opcoes": ["a) farinha ", "b) egg", "c) sugar", "d) all options"],
                "correta": 3},
            {"pergunta": "Which food was at the market?",
                "opcoes": ["a) manteiga ", "b) agua", "c) feijão", "d) biscoito"],
                "correta": 0},
            {"pergunta": "What food is needed for a barbecue(churrasco)?",
                "opcoes": ["a) carne", "b) açúcar", "c) maçã", "d) fermento"],
                "correta": 0}]

    def atualizar(self, eventos):
        if self.concluido:
            # Aguarda 2 segundos antes de finalizar, sem bloquear o jogo
            if pg.time.get_ticks() - self.tempo_fim > 2000:
                return True  # sinaliza que o quiz acabou para a tela principal
            return False

        for evento in eventos:
            if evento.type == pg.KEYDOWN:
                if evento.key == pg.K_w:
                    self.opcao_selecionada = (self.opcao_selecionada - 1) % 4
                    self.som.tocar_click()
                elif evento.key == pg.K_s:
                    self.opcao_selecionada = (self.opcao_selecionada + 1) % 4
                    self.som.tocar_click()
                elif evento.key == pg.K_RETURN:
                    correta = self.perguntas_atuais[self.pergunta_atual]["correta"]
                    if self.opcao_selecionada == correta:
                        self.acertos += 1
                    else:
                        self.erros += 1
                    self.pergunta_atual += 1
                    self.opcao_selecionada = 0
                    self.som.tocar_click()

                    if self.acertos >= 4:
                        self.resultado = "vitoria"
                        self.concluido = True
                        self.tempo_fim = pg.time.get_ticks()
                    elif self.erros >= 2:
                        self.resultado = "refazer"
                        self.concluido = True
                        self.tempo_fim = pg.time.get_ticks()
                    elif self.pergunta_atual >= 5:
                        self.resultado = "vitoria" if self.acertos >= 4 else "refazer"
                        self.concluido = True
                        self.tempo_fim = pg.time.get_ticks()
                    break
        return False

    def desenhar(self, tela):
        tela.fill((0, 0, 0))  # tela preta

        largura_tela = tela.get_width()

        if not self.concluido:
            pergunta = self.perguntas_atuais[self.pergunta_atual]
            
            # Centraliza pergunta
            texto_pergunta = self.fonte_grande.render(pergunta["pergunta"], True, (255, 255, 255))
            rect_pergunta = texto_pergunta.get_rect(center=(largura_tela // 2, 80))
            tela.blit(texto_pergunta, rect_pergunta)

            # Desenha opções
            for i, opcao in enumerate(pergunta["opcoes"]):
                cor = (255, 255, 255) if i == self.opcao_selecionada else (255, 230, 0)
                texto_opcao = self.fonte.render(opcao, True, cor)
                rect_opcao = texto_opcao.get_rect(center=(largura_tela // 2, 180 + i * 60))
                tela.blit(texto_opcao, rect_opcao)

            # Contador de acertos/erros
            texto_contador = self.fonte_contador.render(
                f"Acertos: {self.acertos} | Erros: {self.erros}", True, (255, 255, 255)
            )
            rect_contador = texto_contador.get_rect(center=(largura_tela // 2, 450))
            tela.blit(texto_contador, rect_contador)

        else:
            msg = "Parabéns! Você acertou!" if self.resultado == "vitoria" else "Você errou demais! Tente novamente!"
            cor = (0, 200, 0) if self.resultado == "vitoria" else (200, 0, 0)
            texto = self.fonte_grande.render(msg, True, cor)
            rect_msg = texto.get_rect(center=(largura_tela // 2, 200))
            tela.blit(texto, rect_msg)


    def rodar(self, eventos):
        quiz_finalizado = self.atualizar(eventos)
        self.desenhar(pg.display.get_surface())
        pg.display.flip()
        #self.som.relogio.tick(60)
        if quiz_finalizado:
            return "vitoria" if self.resultado == "vitoria" else "falha"
        return None
