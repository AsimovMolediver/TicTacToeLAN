import pygame
import sys
import requests
import socket
import threading
from tictactoe import *

# Inicialização do Pygame
pygame.init()

# Definições de cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
AZUL = (0, 0, 255)
GREEN = (0, 255, 0)

largura, altura = 300, 300
tamanho_celula = largura // 3  # Divide a largura em 3 para o tabuleiro de jogo da velha
#tela = pygame.display.set_mode((largura, altura))
# Defina a fonte para exibir "X" e "O"
fonte = pygame.font.Font(None, 100)

matriz = setArray()
# Variável para alternar entre "X" e "O"

tabuleiro = [["" for _ in range(3)] for _ in range(3)]

# Configurações da janela
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menu")

def reset_screen():
    global window, WIDTH, HEIGHT
    WIDTH, HEIGHT = 300, 300
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Jogo da velha")

def reset_screen_menu():
    global window, WIDTH, HEIGHT
    # Redefine a largura e altura da tela
    WIDTH, HEIGHT = 800, 600
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Jogo da velha")
def tela_vitoriaX():
    while True:
        window.fill(WHITE)

        draw_text("Vitória do X", font, BLACK, window, WIDTH // 2, HEIGHT // 2)


        # Desenha o botão
        button_width, button_height = 200, 50
        button_x, button_y = (WIDTH - button_width) // 2, (HEIGHT + button_height) // 2  # Ajuste da posição do botão
        draw_button("Menu", font, BLACK, GREEN, window, button_x, button_y, button_width, button_height)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # Verifica se o clique ocorreu dentro da área do botão
                if button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height:
                    main_menu()
def tela_vitoriaO():
    while True:
        window.fill(WHITE)

        draw_text("Vitória do O", font, BLACK, window, WIDTH // 2, HEIGHT // 2)

        # Desenha o botão
        button_width, button_height = 200, 50
        button_x, button_y = (WIDTH - button_width) // 2, (HEIGHT + button_height) // 2  # Ajuste da posição do botão
        draw_button("Menu", font, BLACK, GREEN, window, button_x, button_y, button_width, button_height)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # Verifica se o clique ocorreu dentro da área do botão
                if button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height:
                    main_menu()
def tela_empate():
    while True:
        window.fill(WHITE)

        draw_text("Empate!", font, BLACK, window, WIDTH // 2, HEIGHT // 2)

        # Desenha o botão
        button_width, button_height = 200, 50
        button_x, button_y = (WIDTH - button_width) // 2, (HEIGHT + button_height) // 2  # Ajuste da posição do botão
        draw_button("Menu", font, BLACK, GREEN, window, button_x, button_y, button_width, button_height)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # Verifica se o clique ocorreu dentro da área do botão
                if button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height:
                    main_menu()
def jogar():
    reset_screen()
    global matriz
    matriz = setArray()
    control = True
    jogador = "X"
    while control:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                linha_clicada = y // tamanho_celula
                coluna_clicada = x // tamanho_celula
                if matriz[linha_clicada][coluna_clicada] == "":
                    matriz[linha_clicada][coluna_clicada] = jogador
                    if jogador == "X":
                        jogador = "O"
                    else:
                        jogador = "X"
                if victory(matriz, "O"):
                    tela_vitoriaO()
                    control = False
                    break
                elif victory(matriz, "X"):
                    tela_vitoriaX()
                    control = False
                    break
                elif check_draw(matriz):
                    tela_empate()
                    control = False
                    break
                desenhar_tabuleiro()
        desenhar_tabuleiro()
def jogar_lan():
    reset_screen()
    global matriz
    matriz = setArray()
    jogador = ""
    minha_vez = False
    jogo_em_andamento = True
    resultado = None
    running = True  # Flag para controlar a thread de escuta

    # Criação do socket
    
    try:
        s.connect(("localhost", 5555))
    except:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("localhost", 5555))
        

    # Função de escuta do servidor
    def ouvir_servidor():
        nonlocal jogador, minha_vez, jogo_em_andamento, resultado, running
        global matriz
        while running:
            try:
                data = s.recv(1024).decode()
                if not data:
                    break

                # Identificação do jogador
                if "Jogador X" in data:
                    jogador = "X"
                elif "Jogador O" in data:
                    jogador = "O"
                elif "sua vez" in data.lower():
                    minha_vez = True 

                # Resultado do jogo
                elif "venceu" in data or "Empate" in data:
                    if "X venceu" in data:
                        resultado = "X"
                    elif "O venceu" in data:
                        resultado = "O"
                    else:
                        resultado = "Empate"
                    jogo_em_andamento = False
                    break

                # Atualização do tabuleiro
                elif any(c in data for c in ("X", "O", " ")):
                    linhas = data.splitlines()
                    nova_matriz = [["" for _ in range(3)] for _ in range(3)]
                    pos = 0
                    for linha in linhas:
                        for c in linha:
                            if c in ["X", "O", " "]:
                                nova_matriz[pos // 3][pos % 3] = c if c != " " else ""
                                pos += 1
                    matriz = nova_matriz

            except Exception as e:
                if running:  # Só mostra erro se não foi um encerramento intencional
                    print("Erro na conexão com o servidor:", e)
                break

    # Inicia thread para escutar o servidor
    thread = threading.Thread(target=ouvir_servidor, daemon=True)
    thread.start()

    # Loop principal do jogo
    while jogo_em_andamento:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                jogo_em_andamento = False
                pygame.quit()
                try:
                    s.shutdown(socket.SHUT_RDWR)
                except:
                    pass
                s.close()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN and minha_vez:
                x, y = pygame.mouse.get_pos()
                linha = y // tamanho_celula
                coluna = x // tamanho_celula
                pos = linha * 3 + coluna

                if 0 <= linha < 3 and 0 <= coluna < 3 and matriz[linha][coluna] == "":
                    try:
                        s.sendall(str(pos).encode())
                        minha_vez = False
                    except:
                        jogo_em_andamento = False
                        break

        desenhar_tabuleiro()
        pygame.display.update()

    # Encerramento limpo
    running = False
    try:
        s.shutdown(socket.SHUT_RDWR)
    except:
        pass
    s.close()

    # Exibe o resultado e retorna ao menu
    if resultado == "X":
        tela_vitoriaX()
        return
    elif resultado == "O":
        tela_vitoriaO()
        return
    else:
        tela_empate()
        return



def ranking():
    response = requests.get('http://localhost:5002/score')
    if response.status_code == 200:
        scores = response.json()
        print(f"Pontuação dos jogadores: {scores}")
    else:
        print("Falha ao obter a pontuação.")
        

        
# Fonte e tamanho do texto
font = pygame.font.Font(None, 50)
def desenhar_tabuleiro():
    window.fill(WHITE)
    desenhar_linhas()
    desenhar_jogadas()
    pygame.display.update()


def desenhar_linhas():
    for i in range(1, 3):
        pygame.draw.line(window, BLACK, (0, tamanho_celula * i), (largura, tamanho_celula * i), 4)
        pygame.draw.line(window, BLACK, (tamanho_celula * i, 0), (tamanho_celula * i, altura), 4)


def desenhar_jogadas():
    for linha in range(3):
        for coluna in range(3):
            if matriz[linha][coluna] != "":
                texto = fonte.render(matriz[linha][coluna], True, AZUL)
                centro_x = coluna * tamanho_celula + tamanho_celula // 2
                centro_y = linha * tamanho_celula + tamanho_celula // 2
                window.blit(texto, (centro_x - texto.get_width() // 2, centro_y - texto.get_height() // 2))

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)
def draw_button(text, font, color, bg_color, surface, x, y, width, height):
    pygame.draw.rect(surface, bg_color, (x, y, width, height))
    draw_text(text, font, color, surface, x + width // 2, y + height // 2)
def main_menu():
    reset_screen_menu()
    while True:
        window.fill(WHITE)
        draw_text("Jogo da velha", font, BLACK, window, WIDTH // 2, HEIGHT // 4)

        # Botões do menu
        button_width, button_height = 200, 50
        button_start = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 - button_height // 2 - 25, button_width, button_height)
        button_instrucoes = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 - button_height // 2 + 50, button_width, button_height)
        button_sair = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 - button_height // 2 + 125, button_width, button_height)

        pygame.draw.rect(window, BLACK, button_start)
        pygame.draw.rect(window, BLACK, button_instrucoes)
        pygame.draw.rect(window, BLACK, button_sair)

        draw_text("Local", font, WHITE, window, WIDTH // 2, HEIGHT // 2 - 25)
        draw_text("LAN", font, WHITE, window, WIDTH // 2, HEIGHT // 2 + 50)
        draw_text("Sair", font, WHITE, window, WIDTH // 2, HEIGHT // 2 + 125)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_start.collidepoint(pygame.mouse.get_pos()):
                    jogar()
                elif button_instrucoes.collidepoint(pygame.mouse.get_pos()):
                    jogar_lan()  
                elif button_sair.collidepoint(pygame.mouse.get_pos()):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

if __name__ == "__main__":
    main_menu()
