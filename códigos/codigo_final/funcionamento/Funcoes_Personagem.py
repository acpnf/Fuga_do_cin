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

class Jogador:
    def __init__(self):
        self.largura = TAMANHO_CELULA + 20
        self.altura = TAMANHO_CELULA + 20
        
        self.direcao = 0  
        self.movendo = False
        
        try:
            # Carrega imagens do jogador para esquerda e direita para dar o efeito de corrida animada
            self.animacoes = {
                0: [pygame.image.load(f'jogador_andando_direita_{i}.png').convert_alpha() for i in range(1, 4)],
                1: [pygame.image.load(f'jogador_andando_esquerda_{i}.png').convert_alpha() for i in range(1, 4)]
            }
            
            # Imagem parado para cada direção (usando o primeiro frame de cada animação)
            self.parado = {
                0: self.animacoes[0][0],
                1: self.animacoes[1][0]
            }
            
            # Redimensiona todas as imagens
            for direcao in self.animacoes:
                self.animacoes[direcao] = [
                    pygame.transform.scale(img, (self.largura, self.altura)) 
                    for img in self.animacoes[direcao]
                ]
                self.parado[direcao] = pygame.transform.scale(
                    self.parado[direcao], (self.largura, self.altura))
                
        except:
            # Para o caso de as imagens não existirem, uma alternativa a mais 
            self.parado = {
                0: pygame.Surface((self.largura, self.altura)),
                1: pygame.Surface((self.largura, self.altura))
            }
            self.parado[0].fill(AZUL)       # Direita
            self.parado[1].fill(VERMELHO)  # Esquerda
            
            self.animacoes = {
                0: [self.parado[0].copy() for _ in range(3)],
                1: [self.parado[1].copy() for _ in range(3)]
            }
            print("Imagens do jogador não encontradas. Usando fallback.")
        
        self.frame_atual = 0
        self.contador_frames = 0
        self.velocidade_animacao = 5

    def atualizar_direcao(self, dx): # Função Criada para atualizar a direção do player quando ele trocar a direção
        """Atualiza a direção apenas quando muda entre esquerda/direita"""
        if dx > 0:
            self.direcao = 0  # Direita
        elif dx < 0:
            self.direcao = 1  # Esquerda
        # Para cima/baixo (dy), mantém a direção atual

    def atualizar(self): # Função criada para dar o movimento animado ao personagem
        if self.movendo:
            self.contador_frames += 1
            if self.contador_frames >= self.velocidade_animacao:
                self.contador_frames = 0
                self.frame_atual = (self.frame_atual + 1) % len(self.animacoes[self.direcao])

    def desenhar(self, tela, x, y): #Função para desenhar o personagem 
        if self.movendo:
            tela.blit(self.animacoes[self.direcao][self.frame_atual], (x, y))
        else:
            tela.blit(self.parado[self.direcao], (x, y))

def processar_eventos(jogador_x, jogador_y, labirinto, chaves, saida, chegou_destino, jogador): #Função para processar os eventos que acontecem no jogo com o personagem 
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            return False, jogador_x, jogador_y, True
    
    teclas = pygame.key.get_pressed()
    novo_x, novo_y = jogador_x, jogador_y
    dx = 0  # Mudança na posição horizontal
    
    # Só permite novo movimento se já tiver chegado no destino
    if chegou_destino:
        if teclas[pygame.K_w] or teclas[pygame.K_UP]:
            novo_y -= 1
        elif teclas[pygame.K_s] or teclas[pygame.K_DOWN]:
            novo_y += 1
        elif teclas[pygame.K_a] or teclas[pygame.K_LEFT]:
            novo_x -= 1
            dx = -1
        elif teclas[pygame.K_d] or teclas[pygame.K_RIGHT]:
            novo_x += 1
            dx = 1
        
        # Verifica se o movimento é válido
        if (novo_x, novo_y) != (jogador_x, jogador_y):
            direcao = ''
            if novo_y < jogador_y: direcao = 'N'
            elif novo_y > jogador_y: direcao = 'S'
            elif novo_x < jogador_x: direcao = 'W'
            elif novo_x > jogador_x: direcao = 'E'
            
            if labirinto.maze_map[(jogador_y, jogador_x)][direcao]:
                jogador_x, jogador_y = novo_x, novo_y
                verificar_coleta_chave(jogador_x, jogador_y, chaves)
                chegou_destino = False
                # Atualiza a direção do jogador apenas se for movimento horizontal (para que a animação aconteça)
                if dx != 0:
                    jogador.atualizar_direcao(dx)
    
    # Verifica se chegou na saída com todas as chaves
    if (jogador_x, jogador_y) == saida and all(chave['coletada'] for chave in chaves):
        print("Parabéns! Você escapou do labirinto!")
        return False, jogador_x, jogador_y, True
    
    return True, jogador_x, jogador_y, chegou_destino

def processar_eventos(jogador_x, jogador_y, labirinto, chaves, saida, chegou_destino, jogador): #Função para processar os eventos que acontecem no jogo com o personagem 
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            return False, jogador_x, jogador_y, True
    
    teclas = pygame.key.get_pressed()
    novo_x, novo_y = jogador_x, jogador_y
    dx = 0  # Mudança na posição horizontal
    
    # Só permite novo movimento se já tiver chegado no destino
    if chegou_destino:
        if teclas[pygame.K_w] or teclas[pygame.K_UP]:
            novo_y -= 1
        elif teclas[pygame.K_s] or teclas[pygame.K_DOWN]:
            novo_y += 1
        elif teclas[pygame.K_a] or teclas[pygame.K_LEFT]:
            novo_x -= 1
            dx = -1
        elif teclas[pygame.K_d] or teclas[pygame.K_RIGHT]:
            novo_x += 1
            dx = 1
        
        # Verifica se o movimento é válido
        if (novo_x, novo_y) != (jogador_x, jogador_y):
            direcao = ''
            if novo_y < jogador_y: direcao = 'N'
            elif novo_y > jogador_y: direcao = 'S'
            elif novo_x < jogador_x: direcao = 'W'
            elif novo_x > jogador_x: direcao = 'E'
            
            if labirinto.maze_map[(jogador_y, jogador_x)][direcao]:
                jogador_x, jogador_y = novo_x, novo_y
                verificar_coleta_chave(jogador_x, jogador_y, chaves)
                chegou_destino = False
                # Atualiza a direção do jogador apenas se for movimento horizontal (para que a animação aconteça)
                if dx != 0:
                    jogador.atualizar_direcao(dx)
    
    # Verifica se chegou na saída com todas as chaves
    if (jogador_x, jogador_y) == saida and all(chave['coletada'] for chave in chaves):
        print("Parabéns! Você escapou do labirinto!")
        return False, jogador_x, jogador_y, True
    
    return True, jogador_x, jogador_y, chegou_destino
