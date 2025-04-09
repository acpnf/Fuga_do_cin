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

def carregar_animacao_cracha(tipo): #Função Criada para os crachás ficarem girando no mapa
    animacao = []
    for i in range(0, 4):  
        try:
            img = pygame.image.load(f"sprite_{tipo}{i}.png").convert_alpha()
            img = pygame.transform.scale(img, (TAMANHO_CELULA + 10, TAMANHO_CELULA + 10))
            animacao.append(img)
        except: # Caso em que as imagens não estão baixadas e evitam que o código dê erro 
            surf = pygame.Surface((TAMANHO_CELULA + 10, TAMANHO_CELULA + 10))
            cor = VERMELHO if tipo == "IYODA" else VERDE if tipo == "RICARDO"else AZUL
            surf.fill(cor)
            animacao.append(surf)
            print(f"Imagem sprite_{tipo}{i}.png n�o encontrada. Usando fallback.")
    return animacao


def gerar_chaves(labirinto): #Função criada para gerar aleatoriamente as chaves em pontos do labirinto
    chaves = []
    tipos = ["IYODA", "RICARDO", "SERGIO"]
    nomes = {"IYODA": "Iyoda", "RICARDO": "Ricardo", "SERGIO": "Sergio"}
    cores = {"IYODA": VERMELHO, "RICARDO": VERDE, "SERGIO": AZUL}
    
    animacoes = {tipo: carregar_animacao_cracha(tipo) for tipo in tipos} #Animações dos crachás
    
    for tipo in tipos: #Laço de repetição utilizado para substituir as chaves pelas animações dos crachás, usada para os 3 crachás
        while True:
            x = random.randint(2, COLUNAS - 1)
            y = random.randint(2, LINHAS - 1)
            if (x, y) != (1, 1) and all((x, y) != (chave['x'], chave['y']) for chave in chaves):
                chaves.append({
                    'x': x,
                    'y': y,
                    'nome': nomes[tipo],
                    'tipo': tipo,
                    'cor': cores[tipo],
                    'coletada': False,
                    'imagens': animacoes[tipo],
                    'frame_atual': 0,
                    'contador_frames': 0,
                    'velocidade_animacao': 8 
                })
                break
    return chaves

def desenhar_chaves(tela, chaves): #Função para desenhar os crachás no labirinto
    for chave in chaves:
        if not chave['coletada']:
            
            chave['contador_frames'] += 1
            if chave['contador_frames'] >= chave['velocidade_animacao']:
                chave['contador_frames'] = 0
                chave['frame_atual'] = (chave['frame_atual'] + 1) % 4  # Loop entre 0-3
            
            # Centralização dos crachás no local 
            centro_x = (chave['x'] - 1) * TAMANHO_CELULA + (TAMANHO_CELULA - (TAMANHO_CELULA + 10)) // 2
            centro_y = (chave['y'] - 1) * TAMANHO_CELULA + (TAMANHO_CELULA - (TAMANHO_CELULA + 10)) // 2
            
            # Desenho do crachá 
            img_atual = chave['imagens'][chave['frame_atual']]
            tela.blit(img_atual, (centro_x, centro_y))


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

def desenhar_placar(tela, fonte_titulo, fonte_texto, chaves): #Função criada para desenhar o placar interativo, para indicar os objetos coletados 
    
    # Fundo do placar
    pygame.draw.rect(tela, CINZA, (LARGURA_LAB, 0, LARGURA_PLACAR, ALTURA))
    
    # Título do placar
    titulo = fonte_titulo.render("Status das Chaves", True, PRETO)
    tela.blit(titulo, (LARGURA_LAB + 20, 20))
    
    # Divisória
    pygame.draw.line(tela, CINZA_ESCURO, (LARGURA_LAB, 60), (LARGURA, 60), 2)
    
    # Status de cada chave
    y_offset = 80
    for chave in chaves:
        # Mostra a primeira imagem da animação
        img_pequena = pygame.transform.scale(chave['imagens'][0], (120, 120))
        tela.blit(img_pequena, (LARGURA - LARGURA_PLACAR + 10, y_offset))
        
        # Mostra a situação atual da chave (se foi coletada ou não)
        status = "1/1" if chave['coletada'] else "0/1"
        texto = fonte_titulo.render(f"{chave['nome']}: {status}", True, PRETO)
        tela.blit(texto, (LARGURA - LARGURA_PLACAR + 120, y_offset + 60))
        y_offset += 140  
    
    
    # Divisória entre as instruções e a situação dos crachás
    pygame.draw.line(tela, CINZA_ESCURO, (LARGURA_LAB, 500), (LARGURA, 500), 2)
    
    # Instruções do Jogo
    titulo_instrucoes = fonte_titulo.render("Instruções:", True, PRETO)
    tela.blit(titulo_instrucoes, (LARGURA_LAB + 20, 510))
    
    instrucoes = [
        "- Movimentação: W,A,S,D",
        "- Colete as 3 chaves",
        "- Saída liberada após",
        "  coletar todas"
    ]
    
    for i, linha in enumerate(instrucoes):
        texto = fonte_texto.render(linha, True, PRETO)
        tela.blit(texto, (LARGURA_LAB + 20, 550 + i * 30))

def verificar_coleta_chave(jogador_x, jogador_y, chaves): #Função pra verificar se a chave foi coletada 
    for chave in chaves:
        if not chave['coletada'] and jogador_x == chave['x'] and jogador_y == chave['y']:
            chave['coletada'] = True
            return True
    return False

    
def verificar_vitoria(jogador_x, jogador_y, saida, chaves): #Função para definir se o jogador coletou as 3 chaves e entrou na saída
    if jogador_x == saida[1] and jogador_y == saida[0] and all(chave['coletada'] for chave in chaves):
        print("Parabéns! Você escapou do labirinto!")
        return True
    return False

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


def main(): #Função Princial, para juntar todas as outras funções 
    
    # Inicializa o jogo apenas uma vez
    tela, fonte_titulo, fonte_texto = inicializar_jogo()
    porta_fechada, porta_aberta = carregar_imagens_porta()

    # Mostrar tela inicial
    if not mostrar_tela_inicial(tela):
        pygame.quit()
        return
    
    # Loop principal do jogo (permite reiniciar)
    jogando = True
    while jogando:
        # Configurações iniciais do jogo
        tela.fill(BRANCO)
        labirinto = gerar_labirinto()
        chaves = gerar_chaves(labirinto)
        saida = gerar_saida(labirinto, chaves)
        jogador_x, jogador_y = 1, 1
        rodando = True
        
        # Variáveis para movimento suavizado do  jogador 
        jogador_real_x = (jogador_x - 1) * TAMANHO_CELULA + (TAMANHO_CELULA - (TAMANHO_CELULA + 20)) // 2
        jogador_real_y = (jogador_y - 1) * TAMANHO_CELULA + (TAMANHO_CELULA - (TAMANHO_CELULA + 20)) // 2
        velocidade_movimento = 3
        chegou_destino = True
        
        jogador = Jogador()
        clock = pygame.time.Clock()
        
        try:
            fundo = pygame.image.load('fundo2.png').convert()
            fundo = pygame.transform.scale(fundo, (LARGURA_LAB, ALTURA))
        except:
            fundo = pygame.Surface((LARGURA_LAB, ALTURA))
            fundo.fill((200, 200, 200))
            print("Imagem de fundo não encontrada. Usando fallback.")
        
        # Loop do jogo
        while rodando:
            # Processar eventos do jogo
            rodando, novo_x, novo_y, chegou_destino = processar_eventos(
                jogador_x, jogador_y, labirinto, chaves, saida, chegou_destino, jogador)
            
            if not rodando:
                jogando = False
                break
            
            if novo_x != jogador_x or novo_y != jogador_y:
                jogador_x, jogador_y = novo_x, novo_y
                chegou_destino = False
            
            # Atualiza posição do jogador
            destino_x = (jogador_x - 1) * TAMANHO_CELULA + (TAMANHO_CELULA - jogador.largura) // 2
            destino_y = (jogador_y - 1) * TAMANHO_CELULA + (TAMANHO_CELULA - jogador.altura) // 2
            
            if not chegou_destino:
                diff_x = destino_x - jogador_real_x
                diff_y = destino_y - jogador_real_y
                
                if abs(diff_x) > 0.5:
                    jogador_real_x += diff_x / velocidade_movimento
                    jogador.movendo = True
                else:
                    jogador_real_x = destino_x
                    
                if abs(diff_y) > 0.5:
                    jogador_real_y += diff_y / velocidade_movimento
                    jogador.movendo = True
                else:
                    jogador_real_y = destino_y
                    
                if abs(diff_x) <= 0.5 and abs(diff_y) <= 0.5:
                    chegou_destino = True
                    jogador.movendo = False
            
            # Atualiza animação do jogador
            jogador.atualizar()
            
            # Desenha o labirinto, os coletáveis e o placar do jogo 
            tela.blit(fundo, (0, 0))
            desenhar_labirinto(tela, labirinto)
            desenhar_chaves(tela, chaves)
            desenhar_saida(tela, saida, chaves, porta_fechada, porta_aberta)
            jogador.desenhar(tela, jogador_real_x, jogador_real_y)
            desenhar_placar(tela, fonte_titulo, fonte_texto, chaves)
            
            # Verifica vitória
            if verificar_vitoria(jogador_x, jogador_y, saida, chaves):
                # Mostra tela final com opções
                jogar_novamente = mostrar_tela_final(tela, clock)
                if not jogar_novamente:
                    jogando = False
                break  # Sai do loop do jogo atual
            
            pygame.display.flip()
            clock.tick(60)
    
    pygame.quit()


main()
