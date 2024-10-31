# Configurações iniciais
import pygame
import random

pygame.init()

# Configura o título da janela e define as dimensões da tela
pygame.display.set_caption("Jogo Snake Python")
largura, altura = 1200, 800
tela = pygame.display.set_mode((largura, altura))
relogio = pygame.time.Clock()
ultima_direcao = "DIREITA"  # Inicia a direção da cobra para a direita

# Definição das cores em RGB
preta = (0, 0, 0)
branca = (255, 255, 255)
vermelho = (255, 0, 0)
verde = (0, 255, 0)

# Parâmetros do jogo
tamanho_quadrado = 20  # Tamanho dos blocos da cobra
velocidade_jogo = 15   # Define a velocidade de atualização do jogo

# Função para gerar coordenadas aleatórias para a comida
def gerar_comida():
    comida_x = round(random.randrange(0, largura - tamanho_quadrado) / 20.0) * 20.0
    comida_y = round(random.randrange(0, altura - tamanho_quadrado) / 20.0) * 20.0
    return comida_x, comida_y

# Desenha a comida na tela
def desenhar_comida(tamanho, comida_x, comida_y):
    pygame.draw.rect(tela, vermelho, [comida_x, comida_y, tamanho, tamanho])

# Desenha a cobra na tela
def desenhar_cobra(tamanho, pixels):
    for pixel in pixels:
        pygame.draw.rect(tela, branca, [pixel[0], pixel[1], tamanho, tamanho])

# Desenha a pontuação na tela
def desenhar_pontuacao(pontuacao):
    fonte = pygame.font.SysFont("Helvetica", 35)
    texto = fonte.render(f"Pontos: {pontuacao}", True, verde)
    tela.blit(texto, [1, 1])

# Função para definir a direção da cobra conforme a tecla pressionada
def selecionar_velocidade(tecla):
    global ultima_direcao
    velocidade_x = 0
    velocidade_y = 0

    if tecla == pygame.K_DOWN and ultima_direcao != "CIMA":
        velocidade_x = 0
        velocidade_y = tamanho_quadrado
        ultima_direcao = "BAIXO"
    elif tecla == pygame.K_UP and ultima_direcao != "BAIXO":
        velocidade_x = 0
        velocidade_y = -tamanho_quadrado
        ultima_direcao = "CIMA"
    elif tecla == pygame.K_RIGHT and ultima_direcao != "ESQUERDA":
        velocidade_x = tamanho_quadrado
        velocidade_y = 0
        ultima_direcao = "DIREITA"
    elif tecla == pygame.K_LEFT and ultima_direcao != "DIREITA":
        velocidade_x = -tamanho_quadrado
        velocidade_y = 0
        ultima_direcao = "ESQUERDA"

    return velocidade_x, velocidade_y

# Função principal do jogo
def rodar_jogo():
    fim_jogo = False
    x = largura / 2
    y = altura / 2

    # Define a direção inicial da cobra
    velocidade_x = tamanho_quadrado
    velocidade_y = 0

    tamanho_cobra = 1
    pixels = []

    comida_x, comida_y = gerar_comida()

    while not fim_jogo:
        tela.fill(preta)

        # Verifica os eventos do jogo
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                fim_jogo = True
            elif evento.type == pygame.KEYDOWN:
                nova_velocidade_x, nova_velocidade_y = selecionar_velocidade(evento.key)
                if nova_velocidade_x != 0 or nova_velocidade_y != 0:
                    velocidade_x, velocidade_y = nova_velocidade_x, nova_velocidade_y

        # Desenha a comida
        desenhar_comida(tamanho_quadrado, comida_x, comida_y)

        # Atualiza a posição da cobra
        if x < 0 or x >= largura or y < 0 or y >= altura:
            fim_jogo = True

        x += velocidade_x
        y += velocidade_y

        # Adiciona a nova posição da cabeça da cobra
        pixels.append([x, y])
        if len(pixels) > tamanho_cobra:
            del pixels[0]

        # Verifica se a cobra colidiu com ela mesma
        for pixel in pixels[:-1]:
            if pixel == [x, y]:
                fim_jogo = True

        desenhar_cobra(tamanho_quadrado, pixels)

        # Desenha a pontuação
        desenhar_pontuacao(tamanho_cobra - 1)

        # Atualiza a tela
        pygame.display.update()

        # Gera nova comida ao comer
        if x == comida_x and y == comida_y:
            tamanho_cobra += 1
            comida_x, comida_y = gerar_comida()

        relogio.tick(velocidade_jogo)

# Inicia o jogo
rodar_jogo()
