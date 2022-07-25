import socket
import time


# from board import *
class server:

    def __init__(self):
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        serversocket.bind(('127.0.0.1', 80))

        serversocket.listen(5)

        serversocket.settimeout(5)

        clients = []
        gamenames = []

        # check if all players are ready
        self.ready_count = 0

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
            print('connection with ' + str(address) + ' ' + str(gamename))

            broadcast(f'{gamename} joined'.encode("utf-8"))

            #
            client.send('ready'.encode('utf-8'))
            self.ready_count += (1 if client.recv(1024).decode("utf-8") == "ready" else 0)
            print(self.ready_count)
            broadcast(f'{gamename} is ready'.encode("utf-8"))

            if(len(clients) == self.ready_count):
                Game_Start()

        def Game_Start():
            broadcast(f'all players are ready'.encode("utf-8"))
            broadcast(f'the game is starting'.encode("utf-8"))
            return


        stop = time.time() + 9999
        while time.time() < stop:  ##run startup routine for 30 seconds
            try:
                startup()
            except socket.timeout:
                pass

        broadcast(f"Starting game with {gamenames}".encode("utf-8"))

server()