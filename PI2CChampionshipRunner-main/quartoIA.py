import socket
import json
import sys
import time
import random
from copy import deepcopy

CLIENT_PORT = int(sys.argv[1])
CLIENT_NAME = sys.argv[2]

SERVER_HOST = "localhost"
SERVER_PORT = 3000

print("test")

# === Quarto helpers ===

WINNING_LINES = [
    [0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15],
    [0, 4, 8, 12], [1, 5, 9, 13], [2, 6, 10, 14], [3, 7, 11, 15],
    [0, 5, 10, 15], [3, 6, 9, 12]
]

PIECES = [
    ('clair', 'carré', 'grand', 'pleine'), ('clair', 'carré', 'grand', 'creuse'),
    ('clair', 'carré', 'petit', 'pleine'), ('clair', 'carré', 'petit', 'creuse'),
    ('clair', 'rond', 'grand', 'pleine'), ('clair', 'rond', 'grand', 'creuse'),
    ('clair', 'rond', 'petit', 'pleine'), ('clair', 'rond', 'petit', 'creuse'),
    ('foncé', 'carré', 'grand', 'pleine'), ('foncé', 'carré', 'grand', 'creuse'),
    ('foncé', 'carré', 'petit', 'pleine'), ('foncé', 'carré', 'petit', 'creuse'),
    ('foncé', 'rond', 'grand', 'pleine'), ('foncé', 'rond', 'grand', 'creuse'),
    ('foncé', 'rond', 'petit', 'pleine'), ('foncé', 'rond', 'petit', 'creuse')
]

def is_winning(board):
    for line in WINNING_LINES:
        props = [board[i] for i in line if board[i] is not None]
        if len(props) < 4:
            continue
        for bit in range(4):
            if all((p >> bit) & 1 for p in props) or all(~p >> bit & 1 for p in props):
                return True
    return False

def get_available_positions(board):
    return [i for i in range(16) if board[i] is None]

def get_available_pieces(board):
    return [p for p in range(16) if p not in board and p is not None]

def utility(board):
    return 1 if is_winning(board) else 0

def minimax(board, piece, depth, maximizing):
    if depth == 0 or is_winning(board):
        return utility(board), None, None

    best_score = float('-inf') if maximizing else float('inf')
    best_move, best_piece = None, None

    for pos in get_available_positions(board):
        new_board = board[:]
        new_board[pos] = piece
        if is_winning(new_board):
            score = 1 if maximizing else -1
            return score, pos, None

        for next_piece in get_available_pieces(new_board):
            score, _, _ = minimax(new_board, next_piece, depth - 1, not maximizing)
            if maximizing:
                if score > best_score:
                    best_score = score
                    best_move = pos
                    best_piece = next_piece
            else:
                if score < best_score:
                    best_score = score
                    best_move = pos
                    best_piece = next_piece

    return best_score, best_move, best_piece

# === Réponse au serveur ===

def send_pong(conn):
    response = {"response": "pong"}
    conn.sendall(json.dumps(response).encode())
    print("pong envoyé")

def handle_play(conn, request):
    state = request["state"]
    board = state["board"]
    piece = state["piece"]

    print(f"Type de board : {type(board)}")  
    print(f"Type de piece : {type(piece)}")  

    # Si aucune pièce n'est donnée (premier tour), donne une pièce aléatoire
    if piece is None:
        piece = random.choice(get_available_pieces(board))  # Choisir une pièce valide aléatoire
        print(f"Choix de la première pièce : {piece}")
        response = {
            "response": "move",
            "move": piece,
            "message": f"{CLIENT_NAME} donne la première pièce."
        }
    else:
        print(f"Joueur choisit une pièce : {piece}")
        _, move, next_piece = minimax(board, piece, 2, True)
        print(f"Après minimax, pièce choisie pour le prochain coup : {move}, {next_piece}")

        if move is None:
            response = {"response": "giveup"}
        else:
            response = {
                "response": "move",
                "move": [move, next_piece],
                "message": f"{CLIENT_NAME} joue {piece} en {move} et donne {next_piece}"
            }

    print(f"État du plateau avant l'envoi de la réponse : {board}")
    conn.sendall(json.dumps(response).encode())
    print("Réponse envoyée:", response)

# === Écoute ===

def écoute():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("", CLIENT_PORT))
        s.listen()
        print(f"{CLIENT_NAME} écoute sur le port {CLIENT_PORT}...")

        while True:
            conn, _ = s.accept()
            with conn:
                data = conn.recv(4096).decode()
                if not data:
                    continue
                try:
                    request = json.loads(data)
                except json.JSONDecodeError:
                    conn.sendall(json.dumps({"response": "error", "error": "invalid JSON"}).encode())
                    continue

                req_type = request.get("request")
                if req_type == "ping":
                    send_pong(conn)
                elif req_type == "play":
                    handle_play(conn, request)
                else:
                    conn.sendall(json.dumps({"response": "error", "error": "unknown request"}).encode())

# === Inscription et écoute ===
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((SERVER_HOST, SERVER_PORT))
    subscribe_msg = {
        "request": "subscribe",
        "port": CLIENT_PORT,
        "name": CLIENT_NAME,
        "matricules": [f"{CLIENT_PORT}2", f"{CLIENT_PORT}0"]
    }
    s.sendall(json.dumps(subscribe_msg).encode())
    response = s.recv(4096).decode()
    print("Réponse du serveur:", response)

écoute()

