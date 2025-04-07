import pygame
import random
from pyamaze import maze, COLOR

# Configurações do jogo
LARGURA, ALTURA = 1000, 800
LINHAS, COLUNAS = 20, 20
TAMANHO_CELULA = (LARGURA - 250) // COLUNAS

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
AZUL = (0, 0, 255)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
AMARELO = (255, 255, 0)
ROXO = (128, 0, 128)
CINZA = (200, 200, 200)

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
    pygame.display.set_caption("Labirinto com Chaves")
    fonte = pygame.font.Font(None, 36)
    return tela, fonte

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
    for i in range(0, 4):  # 4 imagens para cada crachá
        try:
            img = pygame.image.load(f"sprite_{tipo}{i}.png").convert_alpha()
            img = pygame.transform.scale(img, (TAMANHO_CELULA // 2, TAMANHO_CELULA // 2))
            animacao.append(img)
        except:
            # Fallback: cria superfície colorida
            surf = pygame.Surface((TAMANHO_CELULA // 2, TAMANHO_CELULA // 2))
            cor = VERMELHO if tipo == "IYODA" else VERDE if tipo == "MASSA" else AZUL
            surf.fill(cor)
            animacao.append(surf)
            print(f"Imagem sprite_{tipo}{i}.png não encontrada. Usando fallback.")
    return animacao

def gerar_chaves(labirinto):
    chaves = []
    tipos = ["IYODA", "MASSA", "SOARES"]
    nomes = {"IYODA": "Iyoda", "MASSA": "Massa", "SOARES": "Soares"}
    cores = {"IYODA": VERMELHO, "MASSA": VERDE, "SOARES": AZUL}
    
    # Pré-carrega as animações para cada tipo de crachá
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
                    'velocidade_animacao': random.randint(5, 10)
                })
                break  # Gera apenas 1 crachá de cada tipo
    return chaves

def desenhar_chaves(tela, chaves):
    for chave in chaves:
        if not chave['coletada']:
            # Atualiza animação
            chave['contador_frames'] += 1
            if chave['contador_frames'] >= chave['velocidade_animacao']:
                chave['contador_frames'] = 0
                chave['frame_atual'] = (chave['frame_atual'] + 1) % 4  # Loop entre 0-3
            
            # Posição central
            centro_x = (chave['x'] - 1) * TAMANHO_CELULA + TAMANHO_CELULA // 2
            centro_y = (chave['y'] - 1) * TAMANHO_CELULA + TAMANHO_CELULA // 2
            
            # Desenha imagem atual
            img_atual = chave['imagens'][chave['frame_atual']]
            rect = img_atual.get_rect(center=(centro_x, centro_y))
            tela.blit(img_atual, rect.topleft)

def gerar_saida(labirinto, chaves):
    while True:
        x = random.randint(2, COLUNAS - 1)
        y = random.randint(2, LINHAS - 1)
        if (x, y) != (1, 1) and all((x, y) != (chave['x'], chave['y']) for chave in chaves):
            return (x, y)

def desenhar_saida(tela, saida, chaves):
    x, y = saida
    todas_coletadas = all(chave['coletada'] for chave in chaves)  # Corrigido para acessar como dicionário
    cor = VERDE if todas_coletadas else CINZA
    pygame.draw.rect(tela, cor, 
                    ((x - 1) * TAMANHO_CELULA + 10,
                     (y - 1) * TAMANHO_CELULA + 10,
                     TAMANHO_CELULA - 20, TAMANHO_CELULA - 20))

def desenhar_painel_status(tela, fonte, chaves):
    largura_painel = 250
    pygame.draw.rect(tela, CINZA, (LARGURA - largura_painel, 0, largura_painel, ALTURA))
    
    titulo = fonte.render("Status das Chaves", True, PRETO)
    tela.blit(titulo, (LARGURA - largura_painel + 20, 20))
    
    y_offset = 80
    for chave in chaves:
        # Mostra a primeira imagem da animação
        img_pequena = pygame.transform.scale(chave['imagens'][0], (20, 20))
        tela.blit(img_pequena, (LARGURA - largura_painel + 20, y_offset))
        
        status = "1/1" if chave['coletada'] else "0/1"
        texto = fonte.render(f"{chave['nome']}: {status}", True, PRETO)
        tela.blit(texto, (LARGURA - largura_painel + 50, y_offset))
        y_offset += 50
    
    y_offset += 30
    pequena_fonte = pygame.font.Font(None, 24)
    instrucoes = [
        "Instruções:",
        "W/↑: Mover para cima",
        "S/↓: Mover para baixo",
        "A/←: Mover para esquerda",
        "D/→: Mover para direita"
    ]
    
    for linha in instrucoes:
        texto = pequena_fonte.render(linha, True, PRETO)
        tela.blit(texto, (LARGURA - largura_painel + 20, y_offset))
        y_offset += 30

def verificar_colisao_chaves(jogador_x, jogador_y, chaves):
    for chave in chaves:
        if not chave['coletada'] and jogador_x == chave['x'] and jogador_y == chave['y']:
            chave['coletada'] = True
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
                if verificar_colisao_chaves(jogador_x, jogador_y, chaves):
                    print(f"Chave coletada!")
                chegou_destino = False
    
    # Verifica se chegou na saída com todas as chaves
    if (jogador_x, jogador_y) == saida and all(chave['coletada'] for chave in chaves):
        print("Parabéns! Você escapou do labirinto!")
        return False, jogador_x, jogador_y, True
    
    return True, jogador_x, jogador_y, chegou_destino  # Este return deve estar no nível da função

def main():
    tela, fonte = inicializar_jogo()
    labirinto = gerar_labirinto()
    chaves = gerar_chaves(labirinto)
    saida = gerar_saida(labirinto, chaves)
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
        desenhar_saida(tela, saida, chaves)
        desenhar_painel_status(tela, fonte, chaves)
        
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
        clock.tick(60)  # 60 FPS
    
    pygame.quit()

if __name__ == "__main__":
    main()