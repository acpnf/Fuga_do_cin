import pygame
import random
from pyamaze import maze
# Configurações do jogo
LARGURA, ALTURA = 1000, 1000  # Aumentar tamanho da tela
LINHAS, COLUNAS = 25, 25  # Labirinto ainda maior
TAMANHO_CELULA = LARGURA // COLUNAS

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
AZUL = (0, 0, 255)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
AMARELO = (255, 255, 0)

def inicializar_jogo():
    pygame.init()
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Jogo de Labirinto com Pygame e Pyamaze")
    return tela

def gerar_labirinto():
    labirinto = maze(LINHAS, COLUNAS)
    labirinto.CreateMaze()
    return labirinto

def desenhar_labirinto(tela, labirinto):
    for celula in labirinto.maze_map:
        x, y = (celula[1] - 1) * TAMANHO_CELULA, (celula[0] - 1) * TAMANHO_CELULA
        if not labirinto.maze_map[celula]["E"]:
            pygame.draw.line(tela, PRETO, (x + TAMANHO_CELULA, y), (x + TAMANHO_CELULA, y + TAMANHO_CELULA), 2)
        if not labirinto.maze_map[celula]["W"]:
            pygame.draw.line(tela, PRETO, (x, y), (x, y + TAMANHO_CELULA), 2)
        if not labirinto.maze_map[celula]["N"]:
            pygame.draw.line(tela, PRETO, (x, y), (x + TAMANHO_CELULA, y), 2)
        if not labirinto.maze_map[celula]["S"]:
            pygame.draw.line(tela, PRETO, (x, y + TAMANHO_CELULA), (x + TAMANHO_CELULA, y + TAMANHO_CELULA), 2)
