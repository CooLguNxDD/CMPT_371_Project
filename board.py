import random
from secrets import choice

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

def buildDeck():
    deck = []
    #example card: Red 7, Green 8, Blue skip
    colours = ["Fire", "Water", "Snow"]
    values = [0, 1 , 2 , 3 , 4 , 5 , 6 , 7 , 8 , 9, 10]
    for colour in colours:
        for value in values:
            deck.insert(-1, [colour, value])
    #print(deck)
    return deck

full_deck = buildDeck()

random.shuffle(full_deck)

#print(full_deck)

"""Draw card function that draws a specified number of cards off the top of the deck
Parameters: numCards -› integer
Return: cardsDrawn -› list
"""
def drawCards (numCards) :
    cardsDrawn = []
    for x in range (numCards):
        cardsDrawn.append (full_deck.pop(0))
    return cardsDrawn

#drawn_cards = drawCards(4)
#print("Drawn Cards are: ", drawn_cards)
#print("Full Deck Now is: ", full_deck)

"""
Print formatted list of player's hand
Parameter: player-›integer, playerHand-›list
Return: None
"""

def showHand (player, playerHand):
    #print("Player {}".format(player+1))
    print("Your Hand")
    print("--------")
    count = 0;
    for card in playerHand:
        print("# ", count, card)
        count = count+1
    print("")

players = []
numPlayers = int (input ("How many players?" ))
for player in range (numPlayers):
    players.append (drawCards(5))

#showHand(0,players[0])
#showHand(1,players[1])
#print("Players  Now is: ", players)
#print("Full Deck Now is: ", full_deck)

#print("testing card pop", full_deck.pop(0))

#game_on = 1

#print(players[0][0][0])

#player_1_score = 0;
#player_2_score = 0;

def play_card_ju():
    game_on = 1
    player_1_score = 0;
    player_2_score = 0;
    while  game_on == 1:
        print("Player 1 score is: ", player_1_score)
        print("Player 2 score is: ", player_2_score)

        print("Player 1. Your turn. Your Hand is:")
        showHand(0, players[0])
        player_1_choice = int (input ("Player 1. Choose your Card" ))

        print("Player 2. Your turn. Your Hand is:")
        showHand(1, players[1])
        player_2_choice = int(input("Player 2. Choose your Card"))

        if players[0][player_1_choice][0] == players[1][player_2_choice][0] :
            #print("tie")
            if players[0][player_1_choice][1] > players[1][player_2_choice][1] :
                print("Player 1's ", players[0][player_1_choice], "Card beat Player 2's " , players[1][player_2_choice])
                player_1_score = player_1_score + 1

            else:
                print("Player 2's ", players[1][player_2_choice], "Card beat Player 1's ", players[0][player_1_choice])
                player_2_score = player_2_score + 1
        else:
            print("Not a tie")
            if players[0][player_1_choice][0] == "Fire":
                if players[1][player_2_choice][0] == "Snow":
                    print("Player 1's ", players[0][player_1_choice], "Card beat Player 2's ", players[1][player_2_choice])
                    player_1_score = player_1_score + 1
                else:
                    print("Player 2's ", players[1][player_2_choice], "Card beat Player 1's ", players[0][player_1_choice])
                    player_2_score = player_2_score + 1
            elif players[0][player_1_choice][0] == "Snow":
                if players[1][player_2_choice][0] == "Water":
                    print("Player 1's ", players[0][player_1_choice], "Card beat Player 2's ", players[1][player_2_choice])
                    player_1_score = player_1_score + 1
                else:
                    print("Player 2's ", players[1][player_2_choice], "Card beat Player 1's ", players[0][player_1_choice])
                    player_2_score = player_2_score + 1
            elif players[0][player_1_choice][0] == "Water":
                if players[1][player_2_choice][0] == "Fire":
                    print("Player 1's ", players[0][player_1_choice], "Card beat Player 2's ", players[1][player_2_choice])
                    player_1_score = player_1_score + 1
                else:
                    print("Player 2's ", players[1][player_2_choice], "Card beat Player 1's ", players[0][player_1_choice])
                    player_2_score = player_2_score + 1
        if player_1_score >= 2 or player_2_score >= 2:
            game_on = 0
            print("Game Over.")
            print("Player 1 score is: ", player_1_score)
            print("Player 2 score is: ", player_2_score)

        else:
            print("Swaping cards now")
            card_swap_1 = full_deck.pop(0)
            card_swap_2 = full_deck.pop(0)
            players[0][player_1_choice] = card_swap_1
            players[1][player_2_choice] = card_swap_2


def play_multi_card_ju(player_a, player_b):
   
    game_on = 1
    player_a_score = 0;
    player_b_score = 0;
    while  game_on == 1:
        print("Player ", player_a, " score is: ", player_a_score)
        print("Player " , player_b ," score is: ", player_b_score)

        print("Player ", player_a, ". Your turn. Your Hand is:")

        showHand(player_a, players[player_a])
        player_a_choice = int (input ( "Player "+ str(player_a) + " Choose your Card " ))
        while player_a_choice > 4:
            player_a_choice = int(input("Player "+ str(player_a) + " choice a vaild card "))
            
    
        print("Player ", player_b)
        print("Your turn. Your Hand is:")
        showHand(player_b, players[player_b])
        player_b_choice = int (input ( "Player "+ str(player_b) + " Choose your Card" ))
        while player_a_choice > 4:
            player_a_choice = int(input("Player "+ str(player_b) + " choice a vaild card "))

    
            

        if players[player_a][player_a_choice][0] == players[player_b][player_b_choice][0] :
            #print("tie")
            if players[player_a][player_a_choice][1] > players[player_b][player_b_choice][1] :
                print("Player ", player_a, "'s ",  players[player_a][player_a_choice], "Card beat Player", player_b , "s " , players[player_b][player_b_choice])
                player_a_score = player_a_score + 1

            else:
                print("Player", player_b, "s ", players[player_b][player_b_choice], "Card beat Player", player_a, "s ", players[player_a][player_a_choice])
                player_b_score = player_b_score + 1
        else:
            print("Not a tie")
            if players[player_a][player_a_choice][0] == "Fire":
                if players[player_b][player_b_choice][0] == "Snow":
                    print("Player ", player_a, "'s ",  players[player_a][player_a_choice], "Card beat Player", player_b , "s " , players[player_b][player_b_choice])
                    player_a_score = player_a_score + 1
                else:
                    print("Player", player_b, "s ", players[player_b][player_b_choice], "Card beat Player", player_a, "s ", players[player_a][player_a_choice])
                    player_b_score = player_b_score + 1
            elif players[player_a][player_a_choice][0] == "Snow":
                if players[player_b][player_b_choice][0] == "Water":
                    print("Player ", player_a, "'s ",  players[player_a][player_a_choice], "Card beat Player", player_b , "s " , players[player_b][player_b_choice])
                    player_a_score = player_a_score + 1
                else:
                   print("Player", player_b, "s ", players[player_b][player_b_choice], "Card beat Player", player_a, "s ", players[player_a][player_a_choice])
                   player_b_score = player_b_score + 1
            elif players[player_a][player_a_choice][0] == "Water":
                if players[player_b][player_b_choice][0] == "Fire":
                    print("Player ", player_a, "'s ",  players[player_a][player_a_choice], "Card beat Player", player_b , "s " , players[player_b][player_b_choice])
                    player_a_score = player_a_score + 1
                else:
                    print("Player", player_b, "s ", players[player_b][player_b_choice], "Card beat Player", player_a, "s ", players[player_a][player_a_choice])
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
            card_swap_1 = full_deck.pop(0)
            card_swap_2 = full_deck.pop(0)
            players[player_a][player_a_choice] = card_swap_1
            players[player_b][player_b_choice] = card_swap_2

def board_game():
    board_size = 10
    player_positions = [0]*numPlayers
    game_on = 1
    while game_on == 1:
        for i in range(len(player_positions)):
            print("It is now player", i, "'s turn to roll")
            roll = input("Press Any button to roll a die")
            r1 = random.randint(1, 3)
            print("You Rolled a", r1)
            temp_position = r1 + player_positions[i]

            if temp_position >= board_size:
                print("Player", i, " Wins")
                game_on = 0
                #return i
            if temp_position in player_positions:
                other_position = player_positions.index(temp_position)
                print("Player ", other_position, " is already on that position. Play card jujitzu to see who gets the square")
                card_play = play_multi_card_ju(i, other_position)
                if card_play == 1:
                    print("Player ", i, "Won. Swapping positions with player", other_position)
                    temp = player_positions[i]
                    player_positions[i] = temp_position
                    player_positions[other_position] = temp
                else:
                    print("Player ", other_position, "Won. No swapping will occur")
            else:
                player_positions[i] = temp_position






board_game()


#play_card_ju()
#play_multi_card_ju(2, 3)


