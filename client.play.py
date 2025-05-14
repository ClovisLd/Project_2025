import random
import json
import socket

# Fonction pour évaluer l'état du jeu
def evaluate_state(board, current_player, players):
    """
    Fonction d'évaluation qui renvoie un score basé sur l'état actuel du jeu.
    Plus le joueur est proche de la ligne d'arrivée, plus la valeur est élevée.
    """
    # Simplification de l'évaluation : ici, on renvoie un score basé sur la position du joueur
    if current_player == players[0]:
        return len([p for p in board if p == current_player])  # Exemple de score
    else:
        return -len([p for p in board if p == current_player])

# Fonction pour obtenir tous les coups possibles
def get_possible_moves(board, current_player):
    """
    Retourne une liste de coups possibles pour le joueur actuel.
    Chaque coup consiste en une position sur le plateau
    """
    # Exemple de génération de coups : nous choisissons des positions vides (simplification)
    moves = []
    for i in range(len(board)):
        if board[i] is None:  # Si la case est vide
            moves.append(i)  # Ajouter cette case comme un coup possible
    return moves

# Fonction pour appliquer un coup
def apply_move(board, move, current_player):
    """
    Applique le coup sur le plateau.
    Ici, on remplace simplement une case vide par le joueur actuel.
    """
    new_board = list(board)
    new_board[move] = current_player
    return new_board

# Fonction pour vérifier si le jeu est terminé
def game_over(board):
    """
    Vérifie si le jeu est terminé.
    Par exemple, si tous les joueurs ont joué, ou si un joueur a atteint sa ligne d'arrivée.
    """
    # Simplification de la fin de jeu : à implémenter selon les règles
    return False

# Fonction Minimax
def minimax(board, depth, maximizing_player, current_player, players, alpha, beta):
    """
    Algorithme Minimax avec élagage alpha-bêta.
    Maximizing player : Le joueur qui essaie de maximiser son score.
    """
    # Évaluer l'état du jeu à la profondeur 0 (fin de jeu ou profondeur maximale)
    if depth == 0 or game_over(board):
        return evaluate_state(board, current_player, players), None

    moves = get_possible_moves(board, current_player)
    
    if maximizing_player:
        max_eval = float('-inf')
        best_move = None
        for move in moves:
            new_board = apply_move(board, move, current_player)
            eval, _ = minimax(new_board, depth - 1, False, current_player, players, alpha, beta)
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        best_move = None
        for move in moves:
            new_board = apply_move(board, move, current_player)
            eval, _ = minimax(new_board, depth - 1, True, current_player, players, alpha, beta)
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, best_move

# Fonction pour calculer le meilleur coup
def compute_best_move(board, players, current_player):
    """
    Utilise Minimax pour déterminer le meilleur coup.
    """
    # Profondeur de recherche (à ajuster selon les besoins)
    depth = 3
    maximizing_player = (current_player == players[0])

    # Alpha-Bêta initialisation
    alpha = float('-inf')
    beta = float('inf')

    _, best_move = minimax(board, depth, maximizing_player, current_player, players, alpha, beta)
    return best_move

# Fonction de traitement des requêtes de jeu
def handle_play(conn, play_data):
    print("Contenu de la requête play :", json.dumps(play_data, indent=2))  # Debug

    # Extraire l'état du jeu et les informations sur le joueur actuel
    board = play_data["board"]
    current_player = play_data["players"][play_data["current"]]
    piece = play_data["piece"]

    # Calculer le meilleur coup en utilisant Minimax
    best_move = compute_best_move(board, play_data["players"], current_player)

    # Réponse avec le coup à jouer
    response = {
        "response": "move",
        "pos": best_move,  # La position où poser la pièce
        "piece": piece,  # La pièce que l'on va donner à l'adversaire
        "message": f"Player {current_player} is playing!"
    }
    
    conn.sendall(json.dumps(response).encode())
    print("Réponse envoyée:", json.dumps(response, indent=2))

# Fonction pour écouter les requêtes du serveur
def listen_for_requests():
    """Écoute les requêtes du serveur"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 8888))  # Port client
        s.listen()
        print(f"Écoute sur le port 8888...")
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

# Envoi de la requête subscribe pour se connecter au serveur
def subscribe():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("localhost", 3000))  # Connexion au serveur
        subscribe_msg = {
            "request": "subscribe",
            "port": 8888,
            "name": "FunQuoridorClient",
            "matricules": ["12345", "67890"]
        }
        s.sendall(json.dumps(subscribe_msg).encode())
        response = s.recv(4096).decode()
        print("Réponse du serveur:", response)

# Fonction pour répondre au ping
def send_pong(conn):
    """Répond à un ping"""
    response = {"response": "pong"}
    conn.sendall(json.dumps(response).encode())
    print("pong envoyé")

# Lancement de l'abonnement et de l'écoute des requêtes
if __name__ == "__main__":
    subscribe()  # Connexion au serveur
    listen_for_requests()  # Écoute des requêtes de jeu
