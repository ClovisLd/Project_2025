import socket
import json

server_ip = "localhost"
port = 3000
with open('request.json') as file:
    request = json.load(file)


with socket.socket() as s:
    s.settimeout(1)
    s.connect((server_ip, port))
    print("connected")
    s.sendall(json.dumps(request['subscribe']).encode('utf-8'))
    print(s.recv(16).decode())

