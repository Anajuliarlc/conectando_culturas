import pygame as pg
import os

class TelaSelecao:
    def __init__(self):
        self.tela = pg.display.get_surface()
        self.fonte = pg.font.SysFont("Arial", 56, bold=True)
        self.opcoes = ["pmasc", "pfem"]
        self.index_selecionado = 0
        self.sprites = self.carregar_sprites()
        self.relogio = pg.time.Clock()

    def carregar_sprites(self):
        cam_base = os.path.join("niveis_data", "personagens_img")

        # Carrega em tamanho original, depois escala manualmente
        imagens = {
            "pmasc": pg.image.load(os.path.join(cam_base, "pmasc_s.png")).convert_alpha(),
            "pfem": pg.image.load(os.path.join(cam_base, "pfem_s.png")).convert_alpha()
        }

        tamanho_desejado = (300, 300)
        for k in imagens:
            imagens[k] = pg.transform.smoothscale(imagens[k], tamanho_desejado)

        return imagens

    def desenhar_interface(self):
        self.tela.fill((0, 0, 0))  # fundo preto

        # Texto de título
        texto = self.fonte.render("Selecione seu personagem (A / D + ENTER):", True, (255, 255, 255))
        texto_rect = texto.get_rect(center=(640, 80))
        self.tela.blit(texto, texto_rect)

        # Posiciona os personagens
        posicoes = [(440, 400), (840, 400)]  # ajustado para acomodar sprites maiores

        for i, nome in enumerate(self.opcoes):
            sprite = self.sprites[nome]
            rect = sprite.get_rect(center=posicoes[i])
            self.tela.blit(sprite, rect)

            if i == self.index_selecionado:
                # contorno com brilho mais para baixo
                brilho = rect.inflate(40, 40)
                brilho.move_ip(0, 20)
                pg.draw.rect(self.tela, (255, 255, 0), brilho, 6, border_radius=12)

    def rodar(self):
        while True:
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    pg.quit()
                    exit()
                elif evento.type == pg.KEYDOWN:
                    if evento.key == pg.K_a:
                        self.index_selecionado = (self.index_selecionado - 1) % len(self.opcoes)
                    elif evento.key == pg.K_d:
                        self.index_selecionado = (self.index_selecionado + 1) % len(self.opcoes)
                    elif evento.key == pg.K_RETURN:
                        return self.opcoes[self.index_selecionado]

            self.desenhar_interface()
            pg.display.flip()
            self.relogio.tick(60)

