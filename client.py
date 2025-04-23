import sys
import socket
import json
import time


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


def Message_recieved(s:socket):
    # this function is called each time a message is recivied
    client, adress = s.accept()
    message = client.recv(4000).decode()
    print(message)
    # resond to the ping of the server with "pong"
    if json.loads(message)["request"] == "ping":
        client.send(json.dumps(
        {"response": "pong"}
        ).encode('utf-8'))
    # respond to the play with "play"
    if json.loads(message)["request"] == "play":
        print("hello")
    
with socket.socket() as s:
    s.bind((server_ip, port))
    s.listen()
    while True:
        Message_recieved(s)
