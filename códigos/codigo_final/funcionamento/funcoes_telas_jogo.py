import pygame
import random
from pyamaze import maze, COLOR

# Configurações do jogo (Em maiúsculo pois são variáveis constantes)
LARGURA, ALTURA = 1200, 900
LARGURA_LAB, LARGURA_PLACAR = 900, 300
LINHAS, COLUNAS = 25, 25
TAMANHO_CELULA = LARGURA_LAB // COLUNAS

# Cores (Em maiúsculo pois são variáveis constantes)
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
AZUL = (0, 0, 255)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
AMARELO = (255, 255, 0)
ROXO = (128, 0, 128)
CINZA = (200, 200, 200)
CINZA_ESCURO = (150, 150, 150)
CINZA_ESCURO2 = (100, 100, 100)  


def mostrar_tela_inicial(tela):
    # Tentativa de carregar a imagem da tela inicial
    try:
        imagem = pygame.image.load('tela inicial.png').convert()  
        imagem = pygame.transform.scale(imagem, (LARGURA, ALTURA)) 
    except: #Caso no qual a imagem não é encontrada
        imagem = pygame.Surface((LARGURA, ALTURA))
        imagem.fill(ROXO)  # Cor de fallback

    tela.blit(imagem, (0, 0))
    pygame.display.flip()

    esperando = True
    while esperando: # Laço de repetição criado para inicialização do jogo
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            if evento.type == pygame.KEYDOWN or evento.type == pygame.MOUSEBUTTONDOWN:
                esperando = False
    return True

def mostrar_tela_final(tela, clock): #Definição da tela final, após o jogador sair do Labirinto 
    
    try:
        imagem = pygame.image.load('tela final.png').convert()
        imagem = pygame.transform.scale(imagem, (LARGURA, ALTURA))
        tela.blit(imagem, (0, 0))
        pygame.display.flip()
    except:
        # Caso para que a imagem da tela final não seja carregada
        tela.fill(VERDE)
        fonte_titulo = pygame.font.SysFont('Arial', 48, bold=True)
        titulo = fonte_titulo.render("Parabéns! Você venceu!", True, BRANCO)
        tela.blit(titulo, (LARGURA//2 - titulo.get_width()//2, ALTURA//4))
    
    # Áreas clicáveis (Jogar Novamente e Sair)
    botao_jogar = pygame.Rect(148, 533, 917, 150)
    botao_sair = pygame.Rect(368, 722, 459, 137)
    
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False  # Sair do jogo
            
            if evento.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                if botao_jogar.collidepoint(mouse_pos):
                    return True  # Jogar novamente
                
                if botao_sair.collidepoint(mouse_pos):
                    return False  # Sair do jogo
                
        clock.tick(60)
