import socket
import threading

HOST = '127.0.0.1'
PORTA = 55556

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORTA))
server.listen()

salas = {}

def broadcast(sala, mensagem):
    for i in salas[sala]:
        if isinstance(mensagem, str):
            mensagem = mensagem.encode()
        i.send(mensagem)

def enviarMensagem(nome, sala, client):
    while True:
        mensagem = client.recv(1024)
        mensagem = f'{nome}: {mensagem.decode()}\n'
        broadcast(sala, mensagem)

while True: 
    client, addr = server.accept()
    client.send(b'XpTo%72')
    sala = client.recv(1024).decode()
    nome = client.recv(1024).decode()
    if sala not in salas.keys():
        salas[sala] = []
    salas[sala].append(client)
    print(f"{nome} entrou na sala {sala}! INFO{addr}")
    broadcast(sala, f'{nome} entrou na sala.\n')
    thread = threading.Thread(target=enviarMensagem, args=(nome, sala, client))
    thread.start()