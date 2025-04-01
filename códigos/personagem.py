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

def desenhar_jogador(tela, jogador_x, jogador_y):
    pygame.draw.rect(tela, AZUL, ((jogador_x - 1) * TAMANHO_CELULA + 5, (jogador_y - 1) * TAMANHO_CELULA + 5, TAMANHO_CELULA - 10, TAMANHO_CELULA - 10))

def movimentação_persongem(jogador_x, jogador_y, labirinto):
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            return False, jogador_x, jogador_y
        elif evento.type == pygame.KEYDOWN:
            if evento.key in [pygame.K_w, pygame.K_UP] and (jogador_y - 1, jogador_x) in labirinto.maze_map and labirinto.maze_map[(jogador_y, jogador_x)]["N"]:
                jogador_y -= 1
            if evento.key in [pygame.K_s, pygame.K_DOWN] and (jogador_y + 1, jogador_x) in labirinto.maze_map and labirinto.maze_map[(jogador_y, jogador_x)]["S"]:
                jogador_y += 1
            if evento.key in [pygame.K_a, pygame.K_LEFT] and (jogador_y, jogador_x - 1) in labirinto.maze_map and labirinto.maze_map[(jogador_y, jogador_x)]["W"]:
                jogador_x -= 1
            if evento.key in [pygame.K_d, pygame.K_RIGHT] and (jogador_y, jogador_x + 1) in labirinto.maze_map and labirinto.maze_map[(jogador_y, jogador_x)]["E"]:
                jogador_x += 1
    return True, jogador_x, jogador_y

