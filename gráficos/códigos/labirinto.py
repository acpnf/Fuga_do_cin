import pygame
import random
from pyamaze import maze

# Configurações do jogo (Resolução da tela e tamanho do labirinto)
LARGURA, ALTURA = 800, 800  
LINHAS, COLUNAS = 20, 20
TAMANHO_CELULA = LARGURA // COLUNAS

# Cores no padrão RGB
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
AZUL = (0, 0, 255)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
AMARELO = (255, 255, 0)

# Inicializar pygame com o nome "Projeto de IP"
pygame.init()
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Projeto de IP")

# Gerar o labirinto
labirinto = maze(LINHAS, COLUNAS)
labirinto.CreateMaze()

# Definir posição inicial do jogador
jogador_x, jogador_y = 1, 1

# Gerar três chaves coloridas aleatoriamente dentro do labirinto
chaves = []
cores_chaves = [VERMELHO, VERDE, AMARELO]
while len(chaves) < 3:
    posicao_chave = (random.randint(1, LINHAS), random.randint(1, COLUNAS))
    if posicao_chave != (1, 1) and posicao_chave in labirinto.maze_map and posicao_chave not in chaves:
        chaves.append((posicao_chave, cores_chaves[len(chaves)]))

# Loop principal
rodando = True
while rodando:
    tela.fill(BRANCO)

    # Desenhar o labirinto
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
    
    # Desenhar chaves (por enquanto são bolinhas menores que o 'jogador')
    for chave in chaves:
        chave_x, chave_y = chave[0][1], chave[0][0]
        pygame.draw.circle(tela, chave[1], ((chave_x - 0.5) * TAMANHO_CELULA, (chave_y - 0.5) * TAMANHO_CELULA), TAMANHO_CELULA // 4)

    # Desenhar o Jogador (Por enquanto é um quadradinho)
    pygame.draw.rect(tela, AZUL, ((jogador_x - 1) * TAMANHO_CELULA + 5, (jogador_y - 1) * TAMANHO_CELULA + 5, TAMANHO_CELULA - 10, TAMANHO_CELULA - 10))

    # Lidar com eventos do teclado
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key in [pygame.K_w, pygame.K_UP] and (jogador_y - 1, jogador_x) in labirinto.maze_map and labirinto.maze_map[(jogador_y, jogador_x)]["N"]:
                jogador_y -= 1
            if evento.key in [pygame.K_s, pygame.K_DOWN] and (jogador_y + 1, jogador_x) in labirinto.maze_map and labirinto.maze_map[(jogador_y, jogador_x)]["S"]:
                jogador_y += 1
            if evento.key in [pygame.K_a, pygame.K_LEFT] and (jogador_y, jogador_x - 1) in labirinto.maze_map and labirinto.maze_map[(jogador_y, jogador_x)]["W"]:
                jogador_x -= 1
            if evento.key in [pygame.K_d, pygame.K_RIGHT] and (jogador_y, jogador_x + 1) in labirinto.maze_map and labirinto.maze_map[(jogador_y, jogador_x)]["E"]:
                jogador_x += 1
    
    pygame.display.flip()

pygame.quit()