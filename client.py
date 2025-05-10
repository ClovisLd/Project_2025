import sys
import socket
import json
import random as rd
import re
from play import play, empty_cell, full_cell




server_ip = "localhost"
port = int(sys.argv[1])

# pattern pour chercher le nom ou la position de l'erreur
pattern = re.compile(r"'([A-Z]{4}|[0-1][0-9])'")


pieces = ['SDEC', 'SDFP', 'SLEC', 'SLFP', 'BDFC', 'BDFP', 'BLEP', 'BDEP', 'SDFC', 'SLEP', 'SLFC', 'BLFP', 'BDEC', 'BLFC', 'SDEP', 'BLEC']
board = []

# connecting to the game server
with socket.socket() as client:
    client.settimeout(5)
    client.connect(("localhost", 3000))
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
    global pieces
    if len(errors) != 0:
        test = pattern.findall(errors[0]["message"])
        if test in pieces:
            pieces.remove(test)
    board = state["board"]
    play(board, client, errors, lives, state, pieces)
    
    if state["piece"] == "null":
        global empty_cell, full_cell
        pieces = ['SDEC', 'SDFP', 'SLEC', 'SLFP', 'BDFC', 'BDFP', 'BLEP', 'BDEP', 'SDFC', 'SLEP', 'SLFC', 'BLFP', 'BDEC', 'BLFC', 'SDEP', 'BLEC']
        board = []
        empty_cell = set(range(16))
        full_cell = set()
    
    


def Message_recieved(s:socket):
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
    
with socket.socket() as s:
    s.bind((server_ip, port))
    s.listen()
    while True:
        Message_recieved(s)
