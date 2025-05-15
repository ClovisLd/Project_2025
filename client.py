import sys
import socket
import json
import random as rd
import re
from play import play, full_cell, Type_left



#172.17.10.133
server_ip = "localhost"
port = int(sys.argv[1])
turn = 0

# pattern pour chercher le nom ou la position de l'erreur
pattern = re.compile(r"\b([A-Z]{4}|\d{2})\b")

# Etat du jeu et liste de piece restante
pieces = ['SDEC', 'SDFP', 'SLEC', 'SLFP', 'BDFC', 'BDFP', 'BLEP', 'BDEP', 'SDFC', 'SLEP', 'SLFC', 'BLFP', 'BDEC', 'BLFC', 'SDEP', 'BLEC']
board = []

# connecting to the game server
with socket.socket() as client:
    client.settimeout(5)
    client.connect((server_ip, 3000))
    print("connected")
    # send a formated json "request" and and check for a response if the connection is established
    client.sendall(json.dumps(
        {"request": "subscribe",
        "port": port,
        "name": sys.argv[2],
        "matricules": [f"1{port}", f"2{port}"]}
        ).encode('utf-8'))
    print(client.recv(32).decode())


def info_state(lives, errors, state, client):
    global pieces, full_cell, turn
        # retire la piece qu'on doit jouer de la liste piece
    if state["piece"] in pieces:
        Type_left(state["piece"])
        pieces.remove(state["piece"])
        
    # regarde si il y a une erreure si il y en a une retirer la pieces de la liste piece
    if len(errors) != 0:
        print(f"\033[31m||Errors:||{errors}\033[0m")
        test = pattern.findall(errors[0]["message"])
        print(state["board"])
        if test:  # Check if test is not empty
            piece_to_remove = test[0]
            test = []
            if piece_to_remove in pieces:
                Type_left(piece_to_remove)
                pieces.remove(piece_to_remove)
                print(f"\033[92mRemoved {piece_to_remove} from pieces\033[0m")

    errors = 0
    board = state["board"]
    print(turn)
    pieces = play(board, client, lives, state, pieces)

    # remet tt a 0 quand une nouvelle partie commence
    if not full_cell:
        if turn > 2:
            pieces = ['SDEC', 'SDFP', 'SLEC', 'SLFP', 'BDFC', 'BDFP', 'BLEP', 'BDEP', 'SDFC', 'SLEP', 'SLFC', 'BLFP', 'BDEC', 'BLFC', 'SDEP', 'BLEC']
            print("new party")
            turn = 0
    
    


def Message_recieved(s:socket):
    global turn
    # this function is called each time a message is recivied
    client, adress = s.accept()
    message = json.loads(client.recv(4000).decode())
    # print(message)
    # resond to the ping of the server with "pong"
    if message["request"] == "ping":
        client.send(json.dumps(
        {"response": "pong"}
        ).encode('utf-8'))
    # respond to the play with "play"
    if message["request"] == "play":
        info_state(message["lives"], message["errors"], message["state"], client)
        turn+=1



with socket.socket() as s:
    s.bind(("0.0.0.0", port))
    s.listen()
    while True:
        Message_recieved(s)
