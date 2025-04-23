import sys
import socket
import json
import random as rd


server_ip = "localhost"
port = int(sys.argv[1])


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
    print(errors)
    client.send(json.dumps(
        {"response": "move",
        "move": {"pos": rd.randint(0,15),
        "piece": f"{rd.choice(['B', 'S'])}"
                 f"{rd.choice(['D', 'L'])}"
                 f"{rd.choice(['E', 'F'])}"
                 f"{rd.choice(['C', 'P'])}"},
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
