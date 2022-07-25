import socket
import threading
import time

from dataclasses import dataclass


@dataclass
class Player:
    client: socket.socket
    game_name = ""
    is_ready = False


# from board import *
class server:

    def __init__(self):
        # multi-threading
        self.lock = threading.Lock()

        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        serversocket.bind(('127.0.0.1', 80))

        serversocket.listen(5)

        serversocket.settimeout(5)

        players = []

        # check if all players are ready
        self.ready_count = 0

        def broadcast(message):
            for player in players:
                player.client.send(message)

        def startup(player):
            # Game name
            player.client.send('gamename'.encode('utf-8'))

            player.game_name = client.recv(1024).decode("utf-8")

            print('connection with ' + str(address) + ' ' + str(player.game_name))

            broadcast(f'{player.game_name} joined'.encode("utf-8"))

            player_ready(player)

        def player_ready(player):
            # player ready
            player.client.send('ready'.encode('utf-8'))
            msg = player.client.recv(1024).decode("utf-8")
            self.ready_count += (1 if msg == "ready" else 0)
            broadcast(f'{player.game_name} is ready'.encode("utf-8"))

            print("ready! ", self.ready_count)
            if len(players) == self.ready_count:
                # if all players are ready
                Game_Start()


        def Game_Start():
            # start board
            broadcast(f'all players are ready'.encode("utf-8"))
            broadcast(f'the game is starting'.encode("utf-8"))

            return

        stop = time.time() + 9999
        while time.time() < stop:  ##run startup routine for 30 seconds
            try:
                client, address = serversocket.accept()
                player = Player(client=client)
                players.append(player)

                threading.Thread(target=startup, args=(player,)).start()
                print("player count: ", len(players))

                #join thread
                #main_thread = threading.currentThread()
                #for t in threading.enumerate():
                #    if t is not main_thread:
                #       t.join()



            except socket.timeout:
                pass

        # broadcast(f"Starting game with {gamenames}".encode("utf-8"))


server()
