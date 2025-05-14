import socket
import json
import random

SERVER_HOST = "localhost"
SERVER_PORT = 3000
CLIENT_PORT = 8888

# Fonction pour répondre au "ping"
def send_pong(conn):
    """Répond à un ping"""
    response = {"response": "pong"}
    conn.sendall(json.dumps(response).encode())
    print("pong envoyé")

# Fonction pour calculer le meilleur coup
def compute_best_move(board, piece):
    """
    Logique pour déterminer le meilleur coup.
    Ici, un exemple simple où le client place une pièce dans la première case vide.
    """
    for i in range(len(board)):
        if board[i] is None:  # Trouver une case vide
            return {"pos": i, "piece": piece}  # Exemple de coup
    return {"pos": None, "piece": None}  # Si pas de coup possible

# Fonction pour répondre à une requête "play"
def handle_play(conn, play_data):
    print("Contenu de la requête play :", json.dumps(play_data, indent=2))  # Debug

    # Extraire l'état du jeu et les informations sur le joueur actuel
    board = play_data["board"]
    current_player = play_data["players"][play_data["current"]]
    piece = play_data["piece"]

    # Déterminer le meilleur coup en fonction de l'état actuel
    move = compute_best_move(board, piece)

    # Réponse avec le coup à jouer
    response = {
        "response": "move",
        "pos": move["pos"],  # La position où poser la pièce
        "piece": move["piece"],  # La pièce que l'on va donner à l'adversaire
        "message": f"Player {current_player} is playing!"
    }
    
    conn.sendall(json.dumps(response).encode())
    print("Réponse envoyée:", json.dumps(response, indent=2))

# Fonction pour écouter les requêtes du serveur
def listen_for_requests():
    """Écoute les requêtes du serveur"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", CLIENT_PORT))
        s.listen()
        print(f"Écoute sur le port {CLIENT_PORT}...")
        while True:
            conn, _ = s.accept()
            with conn:
                data = conn.recv(4096).decode()
                request = json.loads(data)
                if request["request"] == "ping":
                    send_pong(conn)
                elif request["request"] == "play":
                    handle_play(conn, request)
                else:
                    conn.sendall(json.dumps({"response": "error", "error": "unknown request"}).encode())

# 1. Connexion au serveur et envoi de la requête "subscribe"
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    try:
        s.connect((SERVER_HOST, SERVER_PORT))
        subscribe_msg = {
            "request": "subscribe",
            "port": CLIENT_PORT,
            "name": "fun_name_for_the_client",
            "matricules": ["12345", "67890"]
        }
        s.sendall(json.dumps(subscribe_msg).encode())
        response = s.recv(4096).decode()
        print("Réponse du serveur:", response)
    except Exception as e:
        print(f"Erreur de connexion au serveur: {e}")

# 2. Ensuite, on écoute les requêtes ping et play
listen_for_requests()
