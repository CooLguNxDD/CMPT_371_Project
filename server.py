import socket
import time





serversocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)


serversocket.bind(('127.0.0.1',80))

serversocket.listen(5)

serversocket.settimeout(5)

clients = []
gamenames = []

def broadcast(message):
    for client in clients:
        client.send(message)


def startup():
    client, address = serversocket.accept()
    client.send('gamename'.encode('utf-8'))
    clients.append(client)
    gamename = client.recv(1024)
    gamename = gamename.decode("utf-8")
    gamenames.append(gamename)
    print('connection with ' + str(address) + ' '+ str(gamename))
    broadcast(f'{gamename} joined'.encode("utf-8"))
 
stop = time.time() + 30
while time.time() < stop: ##run startup routine for 30 seconds
    try:
        startup()
    except socket.timeout:
        pass


broadcast(f"Starting game with {gamenames}".encode("utf-8"))










