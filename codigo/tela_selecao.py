import pygame as pg
import os

class TelaSelecao:
    def __init__(self, gerenciador_sons):
        self.fonte = pg.font.SysFont("Arial", 56, bold=True)
        self.opcoes = ["pmasc", "pfem"]
        self.index_selecionado = 0
        self.sprites = self.carregar_sprites()
        self.relogio = pg.time.Clock()
        self.sons = gerenciador_sons

    def carregar_sprites(self):
        cam_base = os.path.join("niveis_data", "personagens_img")
        imagens = {
            "pmasc": pg.image.load(os.path.join(cam_base, "pmasc_s.png")).convert_alpha(),
            "pfem": pg.image.load(os.path.join(cam_base, "pfem_s.png")).convert_alpha()
        }

        tamanho_desejado = (300, 300)
        for k in imagens:
            imagens[k] = pg.transform.smoothscale(imagens[k], tamanho_desejado)

        return imagens

    def desenhar_interface(self, tela):
        tela.fill((0, 0, 0))

        texto = self.fonte.render("Selecione seu personagem (A / D + ENTER):", True, (255, 255, 255))
        texto_rect = texto.get_rect(center=(640, 80))
        tela.blit(texto, texto_rect)

        posicoes = [(440, 400), (840, 400)]
        for i, nome in enumerate(self.opcoes):
            sprite = self.sprites[nome]
            rect = sprite.get_rect(center=posicoes[i])
            tela.blit(sprite, rect)

            if i == self.index_selecionado:
                brilho = rect.inflate(40, 40)
                brilho.move_ip(0, 20)
                pg.draw.rect(tela, (255, 255, 0), brilho, 6, border_radius=12)

    def rodar(self):
        tela = pg.display.get_surface()
        if tela is None:
            print("⚠️ AVISO: nenhuma tela inicializada!")
            return

        while True:
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    pg.quit()
                    exit()
                elif evento.type == pg.KEYDOWN:
                    if evento.key == pg.K_a:
                        self.index_selecionado = (self.index_selecionado - 1) % len(self.opcoes)
                        self.sons.tocar_click()
                    elif evento.key == pg.K_d:
                        self.index_selecionado = (self.index_selecionado + 1) % len(self.opcoes)
                        self.sons.tocar_click()
                    elif evento.key == pg.K_RETURN:
                        self.sons.tocar_click()
                        return self.opcoes[self.index_selecionado]

            self.desenhar_interface(tela)
            pg.display.flip()
            self.relogio.tick(60)

