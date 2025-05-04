import sys
import socket
import json
import random as rd
import re




server_ip = "localhost"
port = int(sys.argv[1])

pieces = ['SDEC', 'SDFP', 'SLEC', 'SLFP', 'BDFC', 'BDFP', 'BLEP', 'BDEP', 'SDFC', 'SLEP', 'SLFC', 'BLFP', 'BDEC', 'BLFC', 'SDEP', 'BLEC']
# pattern pour chercher le nom ou la position de l'erreur
pattern = re.compile(r"'([A-Z]{4}|[0-1][0-9])'")

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


def play(lives, errors, state, client):
    # print(errors)
    # try:
    #     pieces.remove(state["piece"])
    # except:
    #     pass
    if len(errors) != 0:
        print(pattern.findall(errors[0]["message"]))
    choix = rd.choice(pieces)
    # pieces.remove(choix)
    client.send(json.dumps(
        {"response": "move",
        "move": {"pos": rd.randint(0,15),
        "piece": choix},
        "message": "Fun message"}
        ).encode('utf-8'))


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
        play(message["lives"], message["errors"], message["state"], client)
    
with socket.socket() as s:
    s.bind((server_ip, port))
    s.listen()
    while True:
        Message_recieved(s)
