# servidor.py
import socket
import threading

board = [" " for _ in range(9)]
jogadores = []
turno = 0
lock = threading.Lock()

def check_vitoria(tab, simbolo):
    for i in range(3):
        if all(tab[i*3 + j] == simbolo for j in range(3)): return True
        if all(tab[j*3 + i] == simbolo for j in range(3)): return True
    if all(tab[i*3 + i] == simbolo for i in range(3)): return True
    if all(tab[(i+1)*2] == simbolo for i in range(3)): return True
    return False

def check_empate(tab):
    return all(cell != " " for cell in tab)

def enviar_tabuleiro():
    board_str = ""
    for i in range(3):
        board_str += "".join(board[i*3:(i+1)*3]) + "\n"
    for jogador in jogadores:
        jogador.sendall(board_str.encode())

def lidar_com_jogador(conn, idx):
    global turno
    simbolo = "X" if idx == 0 else "O"
    conn.sendall(f"Você é o Jogador {simbolo}".encode())

    while True:
        if turno % 2 != idx:
            continue
        conn.sendall(b"Sua vez")
        try:
            pos = int(conn.recv(1024).decode())
        except:
            continue
        with lock:
            if 0 <= pos < 9 and board[pos] == " ":
                board[pos] = simbolo
                enviar_tabuleiro()
                if check_vitoria(board, simbolo):
                    msg = f"{simbolo} venceu!"
                    for j in jogadores:
                        j.sendall(msg.encode())
                    break
                elif check_empate(board):
                    for j in jogadores:
                        j.sendall(b"Empate!")
                    break
                turno += 1
    conn.close()

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("0.0.0.0", 5555))
    s.listen(2)
    print("Servidor pronto. Aguardando jogadores...")

    while len(jogadores) < 2:
        conn, addr = s.accept()
        print(f"Conexão de {addr}")
        jogadores.append(conn)

    for idx, jogador in enumerate(jogadores):
        threading.Thread(target=lidar_com_jogador, args=(jogador, idx)).start()

if __name__ == "__main__":
    main()
