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
