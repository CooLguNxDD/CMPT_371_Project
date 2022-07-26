import socket
import threading
import time

from dataclasses import dataclass
from turtle import position

# from board_server import *
import board_server as broad_event
import game_event_1vs1 as game_event

import json


@dataclass
class Player:
    client: socket.socket
    address: str
    hand: list
    selected_card: list
    score: int  ### needed? should reset?
    game_name = ""
    is_ready = False
    position = 0


# from board import *
class server:

    def __init__(self):

        # multi-threading support
        self.lock = threading.Lock()
        self.game_on = False
        self.starting = False

        # socket
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.IP = socket.gethostbyname(socket.gethostname())
        print(self.IP)
        
        self.serversocket.bind((self.IP, 80))
        self.serversocket.listen(5)
        self.serversocket.settimeout(5)

        # player class
        self.players = []

        # check if all players are ready
        self.ready_count = 0

        # game instance
        self.new_game = []

        self.threads = []

    def broadcast(self, message):
        time.sleep(0.1)
        for player in self.players:
            player.client.send(message)

    def player_startup(self, player):
        try:
            # create game name for each player
            player.client.send("gamename".encode('utf-8'))

            player.game_name = player.client.recv(1024).decode("utf-8")

            self.broadcast(f'{player.game_name} joined'.encode("utf-8"))
            print('connection with ' + str(player.address) + ' ' + str(player.game_name))

            # set player ready
            self.player_ready(player)

        except ConnectionResetError:
            print("player_startup error")
            self.players.remove(player)
            print("player count: ", len(self.players))

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

        # start game
        self.starting = True
        self.game_on = True

    def Main_Game_Start(self):
        self.broadcast("\n ________________________________________________".encode("utf-8"))
        self.broadcast(f"\nplayer count: {len(self.players)}".encode("utf-8"))
        self.broadcast("\nall players are ready".encode("utf-8"))
        self.broadcast("\nGame start!".encode("utf-8"))
        self.broadcast("\n ________________________________________________".encode("utf-8"))

        self.new_game.append(broad_event.board_server(self.players, self.threads, self.lock))
        # self.new_game.append(game_event.game_event_1vs1(self.players[0], self.players[1]))
        self.new_game[0].start_game()

        print("-" * 20)
        print("end game :)")
        print("-" * 20)
        self.game_on = False

        threading.Thread(target=self.restart_game).start()

    def restart_game(self):
        # restart the game
        self.ready_count = 0

        print("-" * 20)
        self.broadcast("the game is restarting".encode("utf-8"))
        print("the game is restarting")
        print("-" * 20)

        self.reset_player()
        return

    # reset all player
    def reset_player(self):
        self.broadcast("current players: ".encode("utf-8"))
        player_info = "["
        for player in self.players:
            player_info += player.game_name + " "
        player_info += "]"
        self.broadcast(player_info.encode("utf-8"))

        threads = []
        for player in self.players:
            threads.append(threading.Thread(target=self.reset_each_player, args=(player,)))



        for t in threads:
            t.start()

        # wait until all players is being reset
        for t in threads:
            t.join()

        return

    # reset each player in thread
    def reset_each_player(self, player):
        player.hand = []
        player.selected_card = []
        player.is_ready = False
        player.score = 0
        self.player_ready(player)
        return

    def start(self):
        stop = time.time() + 9999

        while time.time() < stop:  ##run startup routine for 30 seconds
            try:
                # not accepting new player if the game has started
                if not self.game_on:
                    client, address = self.serversocket.accept()
                    player = Player(client=client, address=address, hand=[], selected_card=[], score=0)
                    self.players.append(player)
                    # start new thread for each player
                    thread = threading.Thread(target=self.player_startup, args=(player,))
                    thread.start()
                    print("player count: ", len(self.players))
                    self.threads.append(thread)

                elif self.game_on and self.starting:
                    # main game event
                    self.Main_Game_Start()
                    self.starting = False

            except socket.timeout:
                pass

        # broadcast(f"Starting game with {gamenames}".encode("utf-8"))


server = server()
server.start()
