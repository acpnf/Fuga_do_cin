import pygame
import random
from pyamaze import maze, COLOR

# Configurações do jogo
LARGURA, ALTURA = 1200, 900
LARGURA_LAB, LARGURA_PLACAR = 900, 300
LINHAS, COLUNAS = 25, 25
TAMANHO_CELULA = LARGURA_LAB // COLUNAS

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
AZUL = (0, 0, 255)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
AMARELO = (255, 255, 0)
ROXO = (128, 0, 128)
CINZA = (200, 200, 200)
CINZA_ESCURO = (150, 150, 150)
CINZA_ESCURO2 = (100, 100, 100)  # Cor para saída bloqueada


class Jogador:
    def __init__(self):
        # Tamanho aumentado do jogador
        self.largura = TAMANHO_CELULA + 20  # 20 pixels maior que a célula
        self.altura = TAMANHO_CELULA + 20
        
        try:
            # Carrega imagens do jogador (substitua pelos seus arquivos)
            self.parado = pygame.image.load('jogador_parado.png').convert_alpha()
            self.parado = pygame.transform.scale(self.parado, (self.largura, self.altura))
            
            self.animacao_andando = [
                pygame.image.load(f'jogador_andando_direita_{i}.png').convert_alpha() for i in range(1, 4)
            ]
            self.animacao_andando = [
                pygame.transform.scale(img, (self.largura, self.altura)) 
                for img in self.animacao_andando
            ]
        except:
            # Fallback caso as imagens não existam
            self.parado = pygame.Surface((self.largura, self.altura))
            self.parado.fill(AZUL)
            self.animacao_andando = [self.parado.copy() for _ in range(3)]
            print("Imagens do jogador não encontradas. Usando fallback.")
        
        self.frame_atual = 0
        self.contador_frames = 0
        self.velocidade_animacao = 5
        self.movendo = False

    def atualizar(self):
        if self.movendo:
            self.contador_frames += 1
            if self.contador_frames >= self.velocidade_animacao:
                self.contador_frames = 0
                self.frame_atual = (self.frame_atual + 1) % len(self.animacao_andando)

    def desenhar(self, tela, x, y):
        if self.movendo:
            tela.blit(self.animacao_andando[self.frame_atual], (x, y))
        else:
            tela.blit(self.parado, (x, y))

def inicializar_jogo():
    pygame.init()
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Jogo de Labirinto com Placar")
    fonte_titulo = pygame.font.SysFont('Arial', 28, bold=True)
    fonte_texto = pygame.font.SysFont('Arial', 24)
    return tela, fonte_titulo, fonte_texto

def gerar_labirinto():
    m = maze(LINHAS, COLUNAS)
    m.CreateMaze(loopPercent=10)
    return m

def desenhar_labirinto(tela, labirinto):
    for i in range(1, COLUNAS + 1):
        for j in range(1, LINHAS + 1):
            cell = labirinto.maze_map[(j, i)]
            x = (i - 1) * TAMANHO_CELULA
            y = (j - 1) * TAMANHO_CELULA
            
            if not cell['N']:
                pygame.draw.line(tela, PRETO, (x, y), (x + TAMANHO_CELULA, y), 2)
            if not cell['S']:
                pygame.draw.line(tela, PRETO, (x, y + TAMANHO_CELULA), 
                               (x + TAMANHO_CELULA, y + TAMANHO_CELULA), 2)
            if not cell['E']:
                pygame.draw.line(tela, PRETO, (x + TAMANHO_CELULA, y), 
                               (x + TAMANHO_CELULA, y + TAMANHO_CELULA), 2)
            if not cell['W']:
                pygame.draw.line(tela, PRETO, (x, y), (x, y + TAMANHO_CELULA), 2)

def carregar_animacao_cracha(tipo):
    animacao = []
    for i in range(0, 4):  # 4 imagens para cada crach�
        try:
            img = pygame.image.load(f"sprite_{tipo}{i}.png").convert_alpha()
            # Alterado para usar o mesmo tamanho do jogador
            img = pygame.transform.scale(img, (TAMANHO_CELULA + 10, TAMANHO_CELULA + 10))
            animacao.append(img)
        except:
            # Fallback: cria superf�cie colorida
            surf = pygame.Surface((TAMANHO_CELULA + 10, TAMANHO_CELULA + 10))
            cor = VERMELHO if tipo == "IYODA" else VERDE if tipo == "RICARDO"else AZUL
            surf.fill(cor)
            animacao.append(surf)
            print(f"Imagem sprite_{tipo}{i}.png n�o encontrada. Usando fallback.")
    return animacao


def gerar_chaves(labirinto):
    chaves = []
    tipos = ["IYODA", "RICARDO", "SERGIO"]
    nomes = {"IYODA": "Iyoda", "RICARDO": "Ricardo", "SERGIO": "Sergio"}
    cores = {"IYODA": VERMELHO, "RICARDO": VERDE, "SERGIO": AZUL}
    
    # Pr�-carrega as anima��es para cada tipo de crach�
    animacoes = {tipo: carregar_animacao_cracha(tipo) for tipo in tipos}
    
    for tipo in tipos:
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
                    'velocidade_animacao': 8  # Valor fixo para todos os crach�s
                })
                break
    return chaves

def desenhar_chaves(tela, chaves):
    for chave in chaves:
        if not chave['coletada']:
            # Atualiza anima��o
            chave['contador_frames'] += 1
            if chave['contador_frames'] >= chave['velocidade_animacao']:
                chave['contador_frames'] = 0
                chave['frame_atual'] = (chave['frame_atual'] + 1) % 4  # Loop entre 0-3
            
            # Posi��o central (ajustada para o novo tamanho)
            centro_x = (chave['x'] - 1) * TAMANHO_CELULA + (TAMANHO_CELULA - (TAMANHO_CELULA + 10)) // 2
            centro_y = (chave['y'] - 1) * TAMANHO_CELULA + (TAMANHO_CELULA - (TAMANHO_CELULA + 10)) // 2
            
            # Desenha imagem atual
            img_atual = chave['imagens'][chave['frame_atual']]
            tela.blit(img_atual, (centro_x, centro_y))


def gerar_saida(labirinto, chaves):
    while True:
        coluna = random.randint(2, COLUNAS - 1)
        linha = random.randint(2, LINHAS - 1)
        if (coluna, linha) != (1, 1) and all((coluna, linha) != (chave['x'], chave['y']) for chave in chaves):
            return (linha, coluna)
    
def carregar_imagens_porta():
    try:
        porta_fechada = pygame.image.load('porta fechada.png').convert_alpha()
        porta_aberta = pygame.image.load('porta aberta.png').convert_alpha()
        # Redimensiona para caber na célula
        porta_fechada = pygame.transform.scale(porta_fechada, (TAMANHO_CELULA, TAMANHO_CELULA))
        porta_aberta = pygame.transform.scale(porta_aberta, (TAMANHO_CELULA - 5, TAMANHO_CELULA - 5))
    except:
        # Fallback simples - retângulos coloridos
        porta_fechada = pygame.Surface((TAMANHO_CELULA - 5, TAMANHO_CELULA - 5))
        porta_fechada.fill(CINZA_ESCURO2)
        porta_aberta = pygame.Surface((TAMANHO_CELULA - 5, TAMANHO_CELULA - 5))
        porta_aberta.fill(ROXO)
        print("Imagens da porta não encontradas. Usando fallback.")

    return porta_fechada, porta_aberta

def desenhar_saida(tela, saida, chaves, porta_fechada, porta_aberta):
    if saida:
        # Verifica se todas as chaves foram coletadas
        todas_coletadas = all(chave['coletada'] for chave in chaves)
        
        # Posição da porta
        x_pos = (saida[1] - 1) * TAMANHO_CELULA + 2
        y_pos = (saida[0] - 1) * TAMANHO_CELULA + 2
        
        # Desenha a imagem apropriada
        if todas_coletadas:
            tela.blit(porta_aberta, (x_pos + 1, y_pos))
        else:
            tela.blit(porta_fechada, (x_pos - 2, y_pos - 2))

def desenhar_placar(tela, fonte_titulo, fonte_texto, chaves):
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
        # Mostra a primeira imagem da animação (mantido pequeno para o painel)
        img_pequena = pygame.transform.scale(chave['imagens'][0], (120, 120))  # Aumentei um pouco
        tela.blit(img_pequena, (LARGURA - LARGURA_PLACAR + 10, y_offset))
        
        status = "1/1" if chave['coletada'] else "0/1"
        texto = fonte_titulo.render(f"{chave['nome']}: {status}", True, PRETO)
        tela.blit(texto, (LARGURA - LARGURA_PLACAR + 120, y_offset + 60))  # Ajuste posição
        y_offset += 140  # Aumentei o espaçamento
    
    
    # Divisória
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

def verificar_coleta_chave(jogador_x, jogador_y, chaves):
    for chave in chaves:
        if not chave['coletada'] and jogador_x == chave['x'] and jogador_y == chave['y']:
            chave['coletada'] = True
            return True
    return False

    
def verificar_vitoria(jogador_x, jogador_y, saida, chaves):
    if jogador_x == saida[1] and jogador_y == saida[0] and all(chave['coletada'] for chave in chaves):
        print("Parabéns! Você escapou do labirinto!")
        return True
    return False


def processar_eventos(jogador_x, jogador_y, labirinto, chaves, saida, chegou_destino):
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            return False, jogador_x, jogador_y, True
    
    teclas = pygame.key.get_pressed()
    novo_x, novo_y = jogador_x, jogador_y
    
    # Só permite novo movimento se já tiver chegado no destino
    if chegou_destino:
        if teclas[pygame.K_w] or teclas[pygame.K_UP]:
            novo_y -= 1
        elif teclas[pygame.K_s] or teclas[pygame.K_DOWN]:
            novo_y += 1
        elif teclas[pygame.K_a] or teclas[pygame.K_LEFT]:
            novo_x -= 1
        elif teclas[pygame.K_d] or teclas[pygame.K_RIGHT]:
            novo_x += 1
        
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
    
    return True, jogador_x, jogador_y, chegou_destino


def mostrar_tela_inicial(tela):
    # Carregar imagem
    try:
        imagem = pygame.image.load('tela inicial.png').convert()  # Altere para o nome do seu arquivo
        imagem = pygame.transform.scale(imagem, (LARGURA, ALTURA))  # Redimensiona para o tamanho da tela
    except:
        imagem = pygame.Surface((LARGURA, ALTURA))
        imagem.fill(ROXO)  # Cor de fallback

    tela.blit(imagem, (0, 0))
    pygame.display.flip()

    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            if evento.type == pygame.KEYDOWN or evento.type == pygame.MOUSEBUTTONDOWN:
                esperando = False
    return True


def main():
    tela, fonte_titulo, fonte_texto = inicializar_jogo()
    porta_fechada, porta_aberta = carregar_imagens_porta()

        # Mostrar tela inicial
    if not mostrar_tela_inicial(tela):
        pygame.quit()
        return
    tela.fill(BRANCO)
        
    tela, fonte_titulo, fonte_texto = inicializar_jogo()
    labirinto = gerar_labirinto()
    chaves = gerar_chaves(labirinto)
    saida = gerar_saida(labirinto, chaves)  # Saída gerada no início
    jogador_x, jogador_y = 1, 1
    rodando = True
    
    # Variáveis para movimento suave
    jogador_real_x = (jogador_x - 1) * TAMANHO_CELULA + (TAMANHO_CELULA - (TAMANHO_CELULA + 20)) // 2
    jogador_real_y = (jogador_y - 1) * TAMANHO_CELULA + (TAMANHO_CELULA - (TAMANHO_CELULA + 20)) // 2
    velocidade_movimento = 3  # Quanto menor, mais lento
    chegou_destino = True
    
    jogador = Jogador()
    clock = pygame.time.Clock()
    
    
    while rodando:
        tela.fill(BRANCO)
        desenhar_labirinto(tela, labirinto)
        desenhar_chaves(tela, chaves)
        desenhar_saida(tela, saida, chaves, porta_fechada, porta_aberta)
        desenhar_placar(tela, fonte_titulo, fonte_texto, chaves)

        if verificar_vitoria(jogador_x, jogador_y, saida, chaves):
            print("Você venceu!")
            rodando = False
            break
        
        # Calcula posição de destino
        destino_x = (jogador_x - 1) * TAMANHO_CELULA + (TAMANHO_CELULA - jogador.largura) // 2
        destino_y = (jogador_y - 1) * TAMANHO_CELULA + (TAMANHO_CELULA - jogador.altura) // 2
        
        # Movimento suave
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
        
        # Atualiza e desenha o jogador
        jogador.atualizar()
        jogador.desenhar(tela, jogador_real_x, jogador_real_y)
        
        # Processa eventos
        rodando, novo_x, novo_y, chegou_destino = processar_eventos(
            jogador_x, jogador_y, labirinto, chaves, saida, chegou_destino)
        
        if novo_x != jogador_x or novo_y != jogador_y:
            jogador_x, jogador_y = novo_x, novo_y
            chegou_destino = False
        
        pygame.display.flip()
        clock.tick(60) 
    
    pygame.quit()


main()