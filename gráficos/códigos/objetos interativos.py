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

def gerar_chaves(labirinto):
    chaves = []
    cores_chaves = [VERMELHO, VERDE, AMARELO]
    while len(chaves) < 3:
        posicao_chave = (random.randint(1, LINHAS), random.randint(1, COLUNAS))
        if posicao_chave != (1, 1) and posicao_chave in labirinto.maze_map and posicao_chave not in chaves:
            chaves.append((posicao_chave, cores_chaves[len(chaves)]))
    return chaves

def desenhar_chaves(tela, chaves):
    for chave in chaves:
        chave_x, chave_y = chave[0][1], chave[0][0]
        pygame.draw.circle(tela, chave[1], ((chave_x - 0.5) * TAMANHO_CELULA, (chave_y - 0.5) * TAMANHO_CELULA), TAMANHO_CELULA // 4)
