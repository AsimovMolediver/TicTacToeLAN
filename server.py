# servidor.py
import socket
import threading

# Variáveis globais (serão reiniciadas a cada partida)
board = []          # Tabuleiro
jogadores = []      # Lista de conexões
turno = 0           # Turno atual
lock = threading.Lock()
turno_event = threading.Event()  # Evento para sincronizar turnos

def check_vitoria(tab, simbolo):
    # Verifica linhas
    for i in range(3):
        if all(tab[i*3 + j] == simbolo for j in range(3)): return True
    # Verifica colunas
    for i in range(3):
        if all(tab[j*3 + i] == simbolo for j in range(3)): return True
    # Verifica diagonais
    if all(tab[i*3 + i] == simbolo for i in range(3)): return True
    if all(tab[(i+1)*2] == simbolo for i in range(3)): return True  # Correção aplicada
    return False

def check_empate(tab):
    return all(cell != " " for cell in tab)

def enviar_tabuleiro():
    board_str = ""
    for i in range(3):
        board_str += "".join(board[i*3:(i+1)*3]) + "\n"
    for jogador in jogadores:
        try:
            jogador.sendall(board_str.encode())
        except:
            pass  # Ignora jogadores desconectados

def lidar_com_jogador(conn, idx):
    global turno
    simbolo = "X" if idx == 0 else "O"
    
    try:
        conn.sendall(f"Você é o Jogador {simbolo}".encode())
        
        while True:
            # Espera até ser o turno do jogador ou o jogo acabar
            while turno != -1 and turno % 2 != idx and len(jogadores) == 2:
                turno_event.wait(0.1)  # Evita loop ativo

            # Sai se o jogo foi finalizado ou se um jogador desconectou
            if turno == -1 or len(jogadores) < 2:
                break

            try:
                conn.sendall(b"Sua vez")
                pos = int(conn.recv(1024).decode())
            except:
                break  # Desconectou

            with lock:
                if 0 <= pos < 9 and board[pos] == " ":
                    board[pos] = simbolo
                    enviar_tabuleiro()

                    if check_vitoria(board, simbolo):
                        msg = f"{simbolo} venceu!"
                        for j in jogadores:
                            j.sendall(msg.encode())
                        turno = -1  # Sinaliza fim do jogo
                        turno_event.set()
                        break
                    elif check_empate(board):
                        for j in jogadores:
                            j.sendall(b"Empate!")
                        turno = -1
                        turno_event.set()
                        break
                    else:
                        turno += 1
                        turno_event.set()
    except Exception as e:
        print(f"Erro: {e}")
    finally:
        conn.close()

def main():
    global board, jogadores, turno
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Permite reusar porta
    s.bind(("0.0.0.0", 5555))
    s.listen(2)
    print("Servidor pronto. Aguardando partidas...")

    while True:  # Loop de partidas
        # Reinicia estado para nova partida
        board = [" " for _ in range(9)]
        jogadores = []
        turno = 0
        turno_event.clear()

        # Aceita 2 jogadores
        print("Aguardando 2 jogadores...")
        while len(jogadores) < 2:
            try:
                conn, addr = s.accept()
                print(f"Conexão de {addr}")
                jogadores.append(conn)
            except:
                break  # Sai se houver erro na aceitação

        if len(jogadores) < 2:  # Se não conseguiu 2 jogadores
            for conn in jogadores:
                conn.close()
            continue

        # Inicia threads
        print("iniciando trheads")
        threads = []
        for idx, jogador in enumerate(jogadores):
            t = threading.Thread(target=lidar_com_jogador, args=(jogador, idx))
            t.start()
            threads.append(t)

        # Espera partida terminar
        print('Esperando a partida terminar')
        for t in threads:
            t.join()

        # Fecha conexões antigas
        print("fechando conexões antigas")
        for conn in jogadores:
            try:
                conn.shutdown(socket.SHUT_RDWR)
            except:
                pass

        jogadores.clear()
        print("Partida encerrada. Reiniciando...\n")

if __name__ == "__main__":
    main()