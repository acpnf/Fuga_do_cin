import pygame
import random
from pyamaze import maze

# Configurações do jogo
LARGURA_TOTAL = 1200
ALTURA = 900
LARGURA_LAB = 900
LARGURA_PLACAR = 300
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

def inicializar_jogo():
    pygame.init()
    tela = pygame.display.set_mode((LARGURA_TOTAL, ALTURA))
    pygame.display.set_caption("Jogo de Labirinto com Placar")
    fonte_titulo = pygame.font.SysFont('Arial', 28, bold=True)
    fonte_texto = pygame.font.SysFont('Arial', 24)
    return tela, fonte_titulo, fonte_texto

def gerar_labirinto():
    labirinto = maze(LINHAS, COLUNAS)
    labirinto.CreateMaze()
    return labirinto

def gerar_chaves(labirinto):
    chaves = []
    cores_chaves = [VERMELHO, VERDE, AMARELO]
    nomes_chaves = ["Vermelha", "Verde", "Amarela"]
    while len(chaves) < 3:
        posicao_chave = (random.randint(1, LINHAS), random.randint(1, COLUNAS))
        if posicao_chave != (1, 1) and posicao_chave in labirinto.maze_map and posicao_chave not in [chave[0] for chave in chaves]:
            chaves.append((posicao_chave, cores_chaves[len(chaves)], nomes_chaves[len(chaves)], False))
    return chaves

def gerar_saida(labirinto, chaves):
    while True:
        posicao_saida = (random.randint(1, LINHAS), random.randint(1, COLUNAS))
        if posicao_saida != (1, 1) and posicao_saida not in [chave[0] for chave in chaves] and posicao_saida in labirinto.maze_map:
            return posicao_saida

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

def desenhar_chaves(tela, chaves):
    for chave in chaves:
        if not chave[3]:
            chave_x, chave_y = chave[0][1], chave[0][0]
            pygame.draw.circle(tela, chave[1], ((chave_x - 0.5) * TAMANHO_CELULA, (chave_y - 0.5) * TAMANHO_CELULA), TAMANHO_CELULA // 4)

def desenhar_saida(tela, saida, chaves_coletadas):
    if saida:
        cor = ROXO if chaves_coletadas else CINZA_ESCURO2
        pygame.draw.rect(tela, cor, ((saida[1] - 1) * TAMANHO_CELULA + 5, (saida[0] - 1) * TAMANHO_CELULA + 5, TAMANHO_CELULA - 10, TAMANHO_CELULA - 10))
        
        # Adicionar um cadeado se as chaves não foram coletadas
        if not chaves_coletadas:
            centro_x = (saida[1] - 0.5) * TAMANHO_CELULA
            centro_y = (saida[0] - 0.5) * TAMANHO_CELULA
            pygame.draw.rect(tela, PRETO, (centro_x - 10, centro_y - 8, 20, 16), 2)
            pygame.draw.arc(tela, PRETO, (centro_x - 8, centro_y - 15, 16, 16), 0, 3.14, 2)

def desenhar_jogador(tela, jogador_x, jogador_y):
    try:
        jogador_img = pygame.image.load(r'D:\Users\tmem\Desktop\projeto de ip\imagens do jogo\direita.png').convert_alpha()
        novo_largura = TAMANHO_CELULA + 20  # Tamanho personalizado
        novo_altura = TAMANHO_CELULA + 20
        jogador_img = pygame.transform.scale(jogador_img, (novo_largura, novo_altura))
    except FileNotFoundError:
        # Fallback para um quadrado azul
        jogador_img = pygame.Surface((TAMANHO_CELULA - 10, TAMANHO_CELULA - 10))
        jogador_img.fill(AZUL)


    #pygame.draw.rect(tela, AZUL, ((jogador_x - 1) * TAMANHO_CELULA + 5, (jogador_y - 1) * TAMANHO_CELULA + 5, TAMANHO_CELULA - 10, TAMANHO_CELULA - 10))
    offset_x = (TAMANHO_CELULA - novo_largura) // 2
    offset_y = (TAMANHO_CELULA - novo_altura) // 2
    pos_x = (jogador_x - 1) * TAMANHO_CELULA + offset_x
    pos_y = (jogador_y - 1) * TAMANHO_CELULA + offset_y
    tela.blit(jogador_img, (pos_x, pos_y))

def desenhar_placar(tela, fonte_titulo, fonte_texto, chaves):
    # Fundo do placar
    pygame.draw.rect(tela, CINZA, (LARGURA_LAB, 0, LARGURA_PLACAR, ALTURA))
    
    # Título do placar
    titulo = fonte_titulo.render("Status das Chaves", True, PRETO)
    tela.blit(titulo, (LARGURA_LAB + 20, 20))
    
    # Divisória
    pygame.draw.line(tela, CINZA_ESCURO, (LARGURA_LAB, 60), (LARGURA_TOTAL, 60), 2)
    
    # Status de cada chave
    for i, chave in enumerate(chaves):
        status = "1/1" if chave[3] else "0/1"
        texto = fonte_texto.render(f"{chave[2]}: {status}", True, PRETO)
        tela.blit(texto, (LARGURA_LAB + 20, 80 + i * 40))
        
        # Mostrar cor da chave (agora em uma coluna separada)
        pygame.draw.rect(tela, chave[1], (LARGURA_LAB + 200, 80 + i * 40, 25, 25))
    
    # Divisória
    pygame.draw.line(tela, CINZA_ESCURO, (LARGURA_LAB, 220), (LARGURA_TOTAL, 220), 2)
    
    # Instruções do Jogo
    titulo_instrucoes = fonte_titulo.render("Instruções:", True, PRETO)
    tela.blit(titulo_instrucoes, (LARGURA_LAB + 20, 240))
    
    instrucoes = [
        "- Movimentação: W,A,S,D",
        "- Colete as 3 chaves",
        "- Saída liberada após",
        "  coletar todas"
    ]
    
    for i, linha in enumerate(instrucoes):
        texto = fonte_texto.render(linha, True, PRETO)
        tela.blit(texto, (LARGURA_LAB + 20, 280 + i * 30))

def verificar_coleta_chave(jogador_x, jogador_y, chaves):
    for i in range(len(chaves)):
        if chaves[i][0] == (jogador_y, jogador_x) and not chaves[i][3]:
            chaves[i] = (chaves[i][0], chaves[i][1], chaves[i][2], True)
            print(f"Chave {chaves[i][2]} coletada!")

def verificar_vitoria(jogador_x, jogador_y, saida, chaves):
    if saida and (jogador_y, jogador_x) == saida and all(chave[3] for chave in chaves):
        return True
    return False

def processar_eventos(jogador_x, jogador_y, labirinto, chaves, saida):
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            return False, jogador_x, jogador_y
        elif evento.type == pygame.KEYDOWN:
            if evento.key in [pygame.K_w, pygame.K_UP] and labirinto.maze_map[(jogador_y, jogador_x)]["N"]:
                jogador_y -= 1
            if evento.key in [pygame.K_s, pygame.K_DOWN] and labirinto.maze_map[(jogador_y, jogador_x)]["S"]:
                jogador_y += 1
            if evento.key in [pygame.K_a, pygame.K_LEFT] and labirinto.maze_map[(jogador_y, jogador_x)]["W"]:
                jogador_x -= 1
            if evento.key in [pygame.K_d, pygame.K_RIGHT] and labirinto.maze_map[(jogador_y, jogador_x)]["E"]:
                jogador_x += 1
    
    verificar_coleta_chave(jogador_x, jogador_y, chaves)
    return True, jogador_x, jogador_y

def main():
    tela, fonte_titulo, fonte_texto = inicializar_jogo()
    labirinto = gerar_labirinto()
    chaves = gerar_chaves(labirinto)
    saida = gerar_saida(labirinto, chaves)  # Saída gerada no início
    jogador_x, jogador_y = 1, 1
    rodando = True
    
    while rodando:
        tela.fill(BRANCO)
        
        # Desenhar labirinto
        desenhar_labirinto(tela, labirinto)
        desenhar_chaves(tela, chaves)
        desenhar_saida(tela, saida, all(chave[3] for chave in chaves))
        desenhar_jogador(tela, jogador_x, jogador_y)
        
        # Desenhar placar
        desenhar_placar(tela, fonte_titulo, fonte_texto, chaves)
        
        if verificar_vitoria(jogador_x, jogador_y, saida, chaves):
            print("Você venceu!")
            break
        
        rodando, jogador_x, jogador_y = processar_eventos(jogador_x, jogador_y, labirinto, chaves, saida)
        pygame.display.flip()
    
    pygame.quit()


main()
