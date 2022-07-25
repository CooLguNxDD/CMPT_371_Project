import socket
import threading
import time

from dataclasses import dataclass

from board_server import *

import json


@dataclass
class Player:
    client: socket.socket
    address: str
    game_name = ""
    is_ready = False
    hand = []


# from board import *
class server:
    def __init__(self):

        # multi-threading support
        self.lock = threading.Lock()
        self.game_on = 0

        # socket
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serversocket.bind(('127.0.0.1', 80))
        self.serversocket.listen(5)
        self.serversocket.settimeout(5)

        # player class
        self.players = []

        # check if all players are ready
        self.ready_count = 0

        # board
        self.board = board_server()

    def broadcast(self, message):
        for player in self.players:
            player.client.send(message)

    def startup(self, player):

        # create game name for each player
        player.client.send("gamename".encode('utf-8'))

        player.game_name = player.client.recv(1024).decode("utf-8")

        self.broadcast(f'{player.game_name} joined'.encode("utf-8"))
        print('connection with ' + str(player.address) + ' ' + str(player.game_name))

        # set player ready
        self.player_ready(player)

        # start game
        self.Game_Start(player)


    def player_ready(self, player):
        # player ready
        player.client.send("ready".encode('utf-8'))

        # msg received
        msg = player.client.recv(1024).decode("utf-8")
        self.broadcast(f'{player.game_name} is ready'.encode("utf-8"))

        # player ready status
        self.ready_count += (1 if msg == "ready" else 0)
        player.is_ready = True

        # thread lock to make sure game starts only if all players are ready
        self.lock.acquire()
        print("ready! ", self.ready_count)
        while len(self.players) != self.ready_count:
            self.game_on = False
            # if all players are ready
        self.lock.release()

        #start game
        self.game_on = True

    def Game_Start(self, player):
        # start game
        if self.game_on:

            player.hand = self.board.drawCards(5)
            # divide card data into header, card_data
            data = "card*"
            data += json.dumps({"cards": player.hand})
            # send info to client
            player.client.send(data.encode('utf-8'))
        return

    def start(self):
        stop = time.time() + 9999
        while time.time() < stop:  ##run startup routine for 30 seconds
            try:
                # not accepting new player if the game has started
                if not self.game_on:
                    client, address = self.serversocket.accept()
                    player = Player(client=client, address=address)
                    self.players.append(player)

                    # start new thread for each player
                    threading.Thread(target=self.startup, args=(player,)).start()
                    print("player count: ", len(self.players))

            except socket.timeout:
                pass

        # broadcast(f"Starting game with {gamenames}".encode("utf-8"))


server = server()
server.start()
