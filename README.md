# 🎮 Jogo da Velha em Rede com Python

Projeto de Jogo da Velha (Tic Tac Toe) desenvolvido em Python com suporte a partidas entre dois jogadores via rede (socket TCP) e uso de threads para controle simultâneo da comunicação.

> ⚠️ A funcionalidade de **ranking** está presente na interface, mas **não está implementada/funcional** neste protótipo.

## 📁 Estrutura dos Arquivos

- `init.py`: Cliente principal. Responsável por iniciar a interface, conectar-se ao servidor e interagir com o jogo.
- `server.py`: Servidor. Aceita conexões de clientes e gerencia o envio e recebimento de dados do jogo.
- `tictactoe.py`: Implementação da lógica do jogo da velha, gerenciamento de estado e detecção de vencedor.

## 🚀 Como Executar

### Pré-requisitos

- Python 3.x
- Biblioteca `pygame` instalada:
  ```bash
  pip install pygame
- Executar o script server.py(configuração de endereço deve ser feita antes)
- Executar init.py

## MODOS DE JOGO

- Local
- Multiplayer LAN


 
