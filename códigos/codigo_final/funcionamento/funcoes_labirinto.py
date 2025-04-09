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

def inicializar_jogo(): #Função criada para dar início ao programa 
    pygame.init()
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("A Fuga do CIn")
    fonte_titulo = pygame.font.SysFont('Arial', 28, bold=True)
    fonte_texto = pygame.font.SysFont('Arial', 24)
    return tela, fonte_titulo, fonte_texto

def gerar_labirinto(): #Função criada para criar o labirinto junto com a biblioteca do pyamaze
    m = maze(LINHAS, COLUNAS)
    m.CreateMaze(loopPercent=10)
    return m

def desenhar_labirinto(tela, labirinto): #Função criada para desenhar o labirinto
    paredes_surface = pygame.Surface((LARGURA_LAB, ALTURA), pygame.SRCALPHA)
    
    for i in range(1, COLUNAS + 1):
        for j in range(1, LINHAS + 1):
            cell = labirinto.maze_map[(j, i)]
            x = (i - 1) * TAMANHO_CELULA
            y = (j - 1) * TAMANHO_CELULA
            
            cor_parede = (0, 0, 0, 180)
            
            if not cell['N']:
                pygame.draw.line(paredes_surface, cor_parede,
                               (x, y), (x + TAMANHO_CELULA, y), 3)
            if not cell['S']:
                pygame.draw.line(paredes_surface, cor_parede,
                               (x, y + TAMANHO_CELULA), 
                               (x + TAMANHO_CELULA, y + TAMANHO_CELULA), 3)
            if not cell['E']:
                pygame.draw.line(paredes_surface, cor_parede,
                               (x + TAMANHO_CELULA, y), 
                               (x + TAMANHO_CELULA, y + TAMANHO_CELULA), 3)
            if not cell['W']:
                pygame.draw.line(paredes_surface, cor_parede,
                               (x, y), (x, y + TAMANHO_CELULA), 3)
    
    tela.blit(paredes_surface, (0, 0))

def gerar_saida(labirinto, chaves): # Função para gerar uma saída aleatória no mapa 
    while True:
        coluna = random.randint(2, COLUNAS - 1)
        linha = random.randint(2, LINHAS - 1)
        if (coluna, linha) != (1, 1) and all((coluna, linha) != (chave['x'], chave['y']) for chave in chaves):
            return (linha, coluna)
        
def carregar_imagens_porta(): #Função para carregar as imagens da porta que será a saída do labirinto
    try:
        porta_fechada = pygame.image.load('porta fechada.png').convert_alpha()
        porta_aberta = pygame.image.load('porta aberta.png').convert_alpha()
        # Redimensiona para caber na célula
        porta_fechada = pygame.transform.scale(porta_fechada, (TAMANHO_CELULA, TAMANHO_CELULA))
        porta_aberta = pygame.transform.scale(porta_aberta, (TAMANHO_CELULA - 5, TAMANHO_CELULA - 5))
    except:
        # Para o caso de não estarem salvas as imagens do jogo 
        porta_fechada = pygame.Surface((TAMANHO_CELULA - 5, TAMANHO_CELULA - 5))
        porta_fechada.fill(CINZA_ESCURO2)
        porta_aberta = pygame.Surface((TAMANHO_CELULA - 5, TAMANHO_CELULA - 5))
        porta_aberta.fill(ROXO)
        print("Imagens da porta não encontradas. Usando fallback.")

    return porta_fechada, porta_aberta

def desenhar_saida(tela, saida, chaves, porta_fechada, porta_aberta): # Função Criada para desenhar a saída 
    if saida:
        # Verifica se todas as chaves foram coletadas
        todas_coletadas = all(chave['coletada'] for chave in chaves)
        
        # Posição da porta
        x_pos = (saida[1] - 1) * TAMANHO_CELULA + 2
        y_pos = (saida[0] - 1) * TAMANHO_CELULA + 2
        
        # Desenha a imagem de forma centralizada
        if todas_coletadas:
            tela.blit(porta_aberta, (x_pos + 1, y_pos))
        else:
            tela.blit(porta_fechada, (x_pos - 2, y_pos - 2))
