import random
from secrets import choice
import time
import game_event_1vs1 as game_event


#Build deck function. Creates a list of cards
"""
def buildDeck():
    deck = []
    #example card: Red 7, Green 8, Blue skip
    colours = ["Fire", "Water", "Snow"]
    values = [0, 1 , 2 , 3 , 4 , 5 , 6 , 7 , 8 , 9, 10]
    for colour in colours:
        for value in values:
            cardval = "{} {}".format(colour, value)
            deck.append(cardval)
    print(deck)
    return deck
"""

class board_server:

    def __init__(self,players,threads,lock):
        #self.full_deck = self.buildDeck()
        #random.shuffle(self.full_deck)
        #print(self.)
        self.players = players
        self.threads = threads
        self.lock = lock
        self.card = [game_event]
      
        


    def buildDeck(self):  ##not used
        deck = []
        # example card: Red 7, Green 8, Blue skip
        colours = ["Fire", "Water", "Snow"]
        values = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        for colour in colours:
            for value in values:
                deck.insert(-1, [colour, value])
        # print(deck)
        return deck

    def broadcast(self, message):
        time.sleep(0.1)
        for player in self.players:
            player.client.send(message)

    """Draw card function that draws a specified number of cards off the top of the deck
    Parameters: numCards -› integer
    Return: cardsDrawn -› list
    """

    def drawCards(self, numCards):  ## not used
        cardsDrawn = []
        for x in range(numCards):
            cardsDrawn.append(self.full_deck.pop(0))
        return cardsDrawn

    """
    Print formatted list of player's hand
    Parameter: player-›integer, playerHand-›list
    Return: None
    """

    def showHand(self, player, playerHand):  ## not used
        print("Player {}".format(player+1))
        print("Your Hand")
        print("--------")
        count = 0
        for card in playerHand:
            print("# ", count, card)
            count = count + 1
        print("")

    def play_card_ju(self): ## not used
        game_on = 1
        player_1_score = 0;
        player_2_score = 0;
        while game_on == 1:
            print("Player 1 score is: ", player_1_score)
            print("Player 2 score is: ", player_2_score)

            print("Player 1. Your turn. Your Hand is:")
            self.showHand(0, self.players[0])
            player_1_choice = int(input("Player 1. Choose your Card"))

            print("Player 2. Your turn. Your Hand is:")
            self.showHand(1, self.players[1])
            player_2_choice = int(input("Player 2. Choose your Card"))

            if self.players[0][player_1_choice][0] == self.players[1][player_2_choice][0]:
                # print("tie")
                if self.players[0][player_1_choice][1] > self.players[1][player_2_choice][1]:
                    print("Player 1's ", self.players[0][player_1_choice], "Card beat Player 2's ",
                          self.players[1][player_2_choice])
                    player_1_score = player_1_score + 1

                else:
                    print("Player 2's ", self.players[1][player_2_choice], "Card beat Player 1's ",
                          self.players[0][player_1_choice])
                    player_2_score = player_2_score + 1
            else:
                print("Not a tie")
                if self.players[0][player_1_choice][0] == "Fire":
                    if self.players[1][player_2_choice][0] == "Snow":
                        print("Player 1's ", self.players[0][player_1_choice], "Card beat Player 2's ",
                              self.players[1][player_2_choice])
                        player_1_score = player_1_score + 1
                    else:
                        print("Player 2's ", self.players[1][player_2_choice], "Card beat Player 1's ",
                              self.players[0][player_1_choice])
                        player_2_score = player_2_score + 1
                elif self.players[0][player_1_choice][0] == "Snow":
                    if self.players[1][player_2_choice][0] == "Water":
                        print("Player 1's ", self.players[0][player_1_choice], "Card beat Player 2's ",
                              self.players[1][player_2_choice])
                        player_1_score = player_1_score + 1
                    else:
                        print("Player 2's ", self.players[1][player_2_choice], "Card beat Player 1's ",
                              self.players[0][player_1_choice])
                        player_2_score = player_2_score + 1
                elif self.players[0][player_1_choice][0] == "Water":
                    if self.players[1][player_2_choice][0] == "Fire":
                        print("Player 1's ", self.players[0][player_1_choice], "Card beat Player 2's ",
                              self.players[1][player_2_choice])
                        player_1_score = player_1_score + 1
                    else:
                        print("Player 2's ", self.players[1][player_2_choice], "Card beat Player 1's ",
                              self.players[0][player_1_choice])
                        player_2_score = player_2_score + 1
            if player_1_score >= 2 or player_2_score >= 2:
                game_on = 0
                print("Game Over.")
                print("Player 1 score is: ", player_1_score)
                print("Player 2 score is: ", player_2_score)

            else:
                print("Swaping cards now")
                card_swap_1 = self.full_deck.pop(0)
                card_swap_2 = self.full_deck.pop(0)
                self.players[0][player_1_choice] = card_swap_1
                self.players[1][player_2_choice] = card_swap_2

    def play_multi_card_ju(self, player_a, player_b):  ## not used

        game_on = 1
        player_a_score = 0
        player_b_score = 0
        while game_on == 1:
            print("Player ", player_a, " score is: ", player_a_score)
            print("Player ", player_b, " score is: ", player_b_score)

            print("Player ", player_a, ". Your turn. Your Hand is:")

            self.showHand(player_a, self.players[player_a])
            player_a_choice = int(input("Player " + str(player_a) + " Choose your Card "))
            while player_a_choice > 4:
                player_a_choice = int(input("Player " + str(player_a) + " choice a vaild card "))

            print("Player ", player_b)
            print("Your turn. Your Hand is:")
            self.showHand(player_b, self.players[player_b])
            player_b_choice = int(input("Player " + str(player_b) + " Choose your Card"))
            while player_a_choice > 4:
                player_a_choice = int(input("Player " + str(player_b) + " choice a vaild card "))

            if self.players[player_a][player_a_choice][0] == self.players[player_b][player_b_choice][0]:
                # print("tie")
                if self.players[player_a][player_a_choice][1] > self.players[player_b][player_b_choice][1]:
                    print("Player ", player_a, "'s ", self.players[player_a][player_a_choice], "Card beat Player",
                          player_b, "s ", self.players[player_b][player_b_choice])
                    player_a_score = player_a_score + 1

                else:
                    print("Player", player_b, "s ", self.players[player_b][player_b_choice], "Card beat Player",
                          player_a, "s ", self.players[player_a][player_a_choice])
                    player_b_score = player_b_score + 1
            else:
                print("Not a tie")
                if self.players[player_a][player_a_choice][0] == "Fire":
                    if self.players[player_b][player_b_choice][0] == "Snow":
                        print("Player ", player_a, "'s ", self.players[player_a][player_a_choice], "Card beat Player",
                              player_b, "s ", self.players[player_b][player_b_choice])
                        player_a_score = player_a_score + 1
                    else:
                        print("Player", player_b, "s ", self.players[player_b][player_b_choice], "Card beat Player",
                              player_a, "s ", self.players[player_a][player_a_choice])
                        player_b_score = player_b_score + 1
                elif self.players[player_a][player_a_choice][0] == "Snow":
                    if self.players[player_b][player_b_choice][0] == "Water":
                        print("Player ", player_a, "'s ", self.players[player_a][player_a_choice], "Card beat Player",
                              player_b, "s ", self.players[player_b][player_b_choice])
                        player_a_score = player_a_score + 1
                    else:
                        print("Player", player_b, "s ", self.players[player_b][player_b_choice], "Card beat Player",
                              player_a, "s ", self.players[player_a][player_a_choice])
                        player_b_score = player_b_score + 1
                elif self.players[player_a][player_a_choice][0] == "Water":
                    if self.players[player_b][player_b_choice][0] == "Fire":
                        print("Player ", player_a, "'s ", self.players[player_a][player_a_choice], "Card beat Player",
                              player_b, "s ", self.players[player_b][player_b_choice])
                        player_a_score = player_a_score + 1
                    else:
                        print("Player", player_b, "s ", self.players[player_b][player_b_choice], "Card beat Player",
                              player_a, "s ", self.players[player_a][player_a_choice])
                        player_b_score = player_b_score + 1
            if player_a_score >= 2 or player_b_score >= 2:
                game_on = 0
                print("Game Over.")
                print("Player A score is: ", player_a_score)
                print("Player B score is: ", player_b_score)
                if player_a_score > player_b_score:
                    return 1
                else:
                    return 2

            else:
                print("Swaping cards now")
                card_swap_1 = self.full_deck.pop(0)
                card_swap_2 = self.full_deck.pop(0)
                self.players[player_a][player_a_choice] = card_swap_1
                self.players[player_b][player_b_choice] = card_swap_2

    def board_game(self):
        board_size = 10
        player_positions = [0] * len(self.players)
        game_on = 1
        while game_on == 1:
            

            for i in range(len(self.players)):

                for thread in self.threads:
                    thread.join()

                
         
                self.broadcast(f"It is now {self.players[i].game_name}'s turn to roll".encode("utf-8"))
                time.sleep(1)
                self.players[i].client.send("roll*".encode("utf-8"))
                self.players[i].client.recv(1024).decode("utf-8")
                r1 = random.randint(1, 3)
                self.broadcast(f"{self.players[i].game_name} Rolled a {r1}".encode("utf-8"))
                temp_position = r1 + player_positions[i]
                self.broadcast(f"{self.players[i].game_name} Rolled a {r1} and landed on {temp_position}".encode("utf-8"))
                if temp_position >= board_size:
                    #print("Player", i, " Wins")
                    print("-" * 20)
                    self.broadcast(f"{self.players[i].game_name} Wins".encode("utf-8"))
                    print("-" * 20)
                    game_on = 0
                    break
                    # return i
                if temp_position in player_positions:
                    other_position = player_positions.index(temp_position)
                    #print("Player ", other_position,
                    #      " is already on that position. Play card jujitzu to see who gets the square")
                    self.broadcast(f"{self.players[other_position].game_name} is already on that position. {self.players[i].game_name} and {self.players[other_position].game_name} card jujitzu to see who gets the square".encode("utf-8"))
                    #card_play = self.play_multi_card_ju(i, other_position)
                    self.card[0] = game_event.game_event_1vs1(self.players[i], self.players[other_position])
                    card_play = self.card[0].start_game()
                    #card_play = 1
                    if card_play == 1:
                        #print("Player ", i, "Won. Swapping positions with player", other_position)
                        self.broadcast(f"{self.players[i].game_name} Won. Swapping positions with player {self.players[other_position].game_name}".encode("utf-8"))
                        temp = player_positions[i]
                        player_positions[i] = temp_position
                        player_positions[other_position] = temp
                    else:
                        #print("Player ", other_position, "Won. No swapping will occur")
                        self.broadcast(f"{self.players[other_position].game_name} Won. Swapping positions with player {self.players[i].game_name}".encode("utf-8"))
                else:
                    player_positions[i] = temp_position

    def start_game(self):
        print("starting game")
        self.board_game()
        


#board_game()

#play_card_ju()
#play_multi_card_ju(2, 3)


