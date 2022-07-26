from collections import defaultdict

from board_server import *
import json
import threading
import queue
import time


# 1v1 game event
class game_event_1vs1:
    def __init__(self, player1, player2):
        # board
        #self.board = board_server()

        # players
        self.player_1 = player1
        self.player_2 = player2

        ## if goes back to zero
        self.player_1.score = 0 
        self.player_2.score = 0

        self.card_num = 5

        # game is running or not
        self.game_on = True

        # lock
        self.lock = threading.Lock()

        self.full_deck = self.buildDeck()

        random.shuffle(self.full_deck)

    def buildDeck(self):
        deck = []
        # example card: Red 7, Green 8, Blue skip
        colours = ["Fire", "Water", "Snow"]
        values = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        for colour in colours:
            for value in values:
                deck.insert(-1, [colour, value])
        # print(deck)
        return deck

    def drawCards(self, numCards):
        cardsDrawn = []
        for x in range(numCards):
            cardsDrawn.append(self.full_deck.pop(0))
        return cardsDrawn

    # draw cards
    def player_draw_card(self, player, draw_num):
        # draw card
        temp_card = player.hand
        draw_cards = self.drawCards(draw_num)

        for card in draw_cards:
            temp_card.append(card)

        print(temp_card)
        # show hand
        self.player_show_hand(temp_card, player)
        return temp_card

    def player_show_hand(self, card, player):
        # divide card data into header, card_data
        data = "card*"
        data += json.dumps({"cards": card})
        # send info to client
        player.client.send(data.encode('utf-8'))
        return

    # each player plays the selected card
    def player_play_card(self, player):
        try:
            data = "selectedCard*" + str(self.card_num)
            player.client.send(data.encode('utf-8'))
            msg = int(player.client.recv(1024).decode("utf-8"))

            print(f"{player.game_name} played: ", player.hand[msg])
            player.selected_card = player.hand[msg]

            # remove
            del player.hand[msg]

        except Exception as e:
            print("player_play_card error")
            self.game_on = False
            print(e)
        return

    # each player plays one card
    def play_card(self, player1, player2):
        running_thread = []
        try:
            running_thread.append(threading.Thread(target=self.player_play_card, args=(player1,)))
            running_thread.append(threading.Thread(target=self.player_play_card, args=(player2,)))

            # let player select and play their card
            for t in running_thread:
                t.start()

            # wait until all players played their card
            for t in running_thread:
                t.join()

        except Exception as e:
            print("play_card error")
            print(e)
        return

    # broadcast message to both player
    def broadcast(self, message):
        try:
            time.sleep(0.1)
            self.player_1.client.send(message.encode("utf-8"))
            time.sleep(0.1)
            self.player_2.client.send(message.encode("utf-8"))
        except Exception as e:
            self.game_on = False
            print("broadcast error")
            print(e)
        return

    
    def win_condition(self):
        # counter list
        condition_dict = {'Fire': 'Snow', 'Snow': 'Water', 'Water': 'Fire'}

        # same elements
        if self.player_1.selected_card[0] == self.player_2.selected_card[0]:
            # same number
            if self.player_1.selected_card[1] == self.player_2.selected_card[1]:
                self.broadcast("tie")
                self.broadcast(" ")
            # a > b
            elif self.player_1.selected_card[1] > self.player_2.selected_card[1]:
                self.player_1.score += 1
                self.broadcast(f"--------{self.player_1.game_name} win--------")
                self.broadcast(" ")
            # b < a
            else:
                self.player_2.score += 1
                self.broadcast(f"--------{self.player_2.game_name} win--------")
                self.broadcast(" ")
        else:
            #print(condition_dict[self.player_1.selected_card[0]])
            #print(self.player_2.selected_card[0])
            # a counter b
            if condition_dict[self.player_1.selected_card[0]] == self.player_2.selected_card[0]:
                self.player_1.score += 1
                self.broadcast(f"--------{self.player_1.game_name} win--------")
                self.broadcast(" ")
            # b counter a
            else:
                self.player_2.score += 1
                self.broadcast(f"--------{self.player_2.game_name} win--------")
                self.broadcast(" ")
    

    



    def start_game(self):
        print("starting game")
        ret = self.play_multi_card_ju()
        return ret

    def play_multi_card_ju(self):

        time.sleep(0.5)

        self.player_1.hand = self.player_draw_card(self.player_1, self.card_num)
        self.player_2.hand = self.player_draw_card(self.player_2, self.card_num)

        # added delay to make sure two players are in sync
        while self.game_on:

            self.play_card(self.player_1, self.player_2)
            time.sleep(0.5)

            self.broadcast(" ")
            self.broadcast((str(self.player_1.game_name) + " played: " + str(self.player_1.selected_card)))
            self.broadcast((str(self.player_2.game_name) + " played: " + str(self.player_2.selected_card)))
            self.broadcast(" ")

            time.sleep(0.5)
            self.win_condition()

            if self.player_1.score >= 2 or self.player_2.score >= 2:
                self.game_on = False
                self.broadcast("-" * 20)
                self.broadcast("Game Over.")
                self.broadcast(("Player " + str(self.player_1.game_name) + " score is: " + str(self.player_1.score)))
                self.broadcast("Player " + str(self.player_2.game_name) + " score is: " + str(self.player_2.score))
                self.broadcast("-" * 20)
                if self.player_1.score > self.player_2.score:
                     return 1
                else:
                    return 2
            else:
                self.player_1.hand = self.player_draw_card(self.player_1, 1)
                self.player_2.hand = self.player_draw_card(self.player_2, 1)

                self.broadcast(" ")
                self.broadcast(("Player " + str(self.player_1.game_name) + " score is: " + str(self.player_1.score)))
                self.broadcast("Player " + str(self.player_2.game_name) + " score is: " + str(self.player_2.score))
                self.broadcast(" ")

        return
