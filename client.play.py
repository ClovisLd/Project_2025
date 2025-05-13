import socket
import json

SERVER_HOST = "localhost"
SERVER_PORT = 3000
CLIENT_PORT = 8888

def send_pong(conn):
    """Répond à un ping"""
    response = {"response": "pong"}
    conn.sendall(json.dumps(response).encode())
    print("pong envoyé")

def handle_play(conn, play_data):
    print("Contenu de la requête play :", json.dumps(play_data, indent=2))  # 👈 Ajout ici

    """Répond à une requête de jeu"""
    move = "example_move"  # À adapter selon le jeu
    response = {
        "response": "move",
        "move": move,
        "message": "I'm playing!"
    }
    conn.sendall(json.dumps(response).encode())
    print("play envoyé")

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

# 1. Envoie de la requête de subscribe avec un with
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
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

# 2. Ensuite, on écoute les requêtes ping et play
listen_for_requests()
