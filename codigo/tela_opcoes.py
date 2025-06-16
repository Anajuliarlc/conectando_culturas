import pygame as pg
from gerenciador_sons import GerenciadorSons

class TelaOpcoes:
    def __init__(self, gerenciador_sons, voltar_para_jogo=True):
        self.tela = pg.display.get_surface()
        self.relogio = pg.time.Clock()
        self.fonte = pg.font.SysFont("Arial", 48, bold=True)
        self.opcoes = ["Volume Música", "Volume SFX", "Voltar"]
        self.index = 0
        self.sons = gerenciador_sons

        # Inicializa com os volumes atuais
        self.volume_musica = self.sons.volume_musica
        self.volume_sfx = self.sons.volume_sfx

    def desenhar(self):
        self.tela.fill((0, 0, 0))  # Fundo preto

        for i, texto in enumerate(self.opcoes):
            cor_caixa = (255, 255, 255) if i == self.index else (255, 230, 0)
            texto_cor = (0, 0, 0)

            label = texto
            if i == 0:
                label += f": {int(self.sons.volume_musica * 100)}%"
            elif i == 1:
                label += f": {int(self.sons.volume_sfx * 100)}%"

            rend = self.fonte.render(label, True, texto_cor)
            rect = rend.get_rect(center=(672, 250 + i * 100))

            pg.draw.rect(self.tela, cor_caixa, rect.inflate(40, 20), border_radius=10)
            self.tela.blit(rend, rect)

    def rodar(self):
        while True:
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    pg.quit()
                    exit()
                elif e.type == pg.KEYDOWN:
                    if e.key == pg.K_w:
                        self.index = (self.index - 1) % len(self.opcoes)
                        self.sons.tocar_click()
                    elif e.key == pg.K_s:
                        self.index = (self.index + 1) % len(self.opcoes)
                        self.sons.tocar_click()
                    elif e.key == pg.K_a:
                        if self.index == 0:
                            self.volume_musica = max(0.0, self.volume_musica - 0.1)
                            self.sons.ajustar_volume_musica(-0.1)
                        elif self.index == 1:
                            self.volume_sfx = max(0.0, self.volume_sfx - 0.1)
                            self.sons.ajustar_volume_sfx(-0.1)

                    elif e.key == pg.K_d:
                        if self.index == 0:
                            self.volume_musica = min(1.0, self.volume_musica + 0.1)
                            self.sons.ajustar_volume_musica(0.1)
                        elif self.index == 1:
                            self.volume_sfx = min(1.0, self.volume_sfx + 0.1)
                            self.sons.ajustar_volume_sfx(0.1)
                    elif e.key == pg.K_RETURN:
                        self.sons.tocar_click()
                        return True  # Sempre volta ao jogo

            self.desenhar()
            pg.display.flip()
            self.relogio.tick(60)

