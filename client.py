import json
import socket
import threading


# input target ip + port
def target_server():
    IP = ""
    port_number = 0
    while IP == "" and port_number == 0:
        try:
            IP = input("enter a ip:")

            port_number = int(input("enter a port_number:"))
        except:
            print("something is going wrong!")

    return IP, port_number



#check invalid message with target
def msg_check(target_message, except_msg):
    msg = ""
    while msg == "":
        try:
            msg = str(input(target_message))
        except Exception as e:
            print(e)
            print(except_msg)

    return msg

#check invalid message with target
def msg_check_target(target, target_message, except_msg):
    msg = ""
    while msg != target:
        try:
            msg = str(input(target_message))
        except Exception as e:
            print(e)
            print(except_msg)

    return msg

# send game name to server
def set_game_name(client):
    msg = msg_check("input your name\n", "invalid name, please input again\n")
    try:
        client.send(msg.encode())
    except Exception as e:
        print(e)
    return

# send ready to server
def ready(client):
    ready_msg = msg_check_target("ready", "Input \"ready\" if you are ready \n", "Input \"ready\" if you are ready \n")
    try:
        client.send(ready_msg.encode())
    except Exception as e:
        print(e)
    return

# show card on hand
def show_card(message):
    cards = json.loads(message).get("cards")
    showHand(cards)
    return

# show card on hand
def play_card(card_limit, client):
    card_limit = int(card_limit)
    card_index = -1
    try:
        while 0 > card_index or card_index > card_limit:
            card_index = int(input(f"Select a card ({0} - {card_limit - 1}): \n"))
        client.send(str(card_index).encode())
    except Exception as e:
        print(e)
    return

# show card on hand
def showHand(playerHand):
    # print("Player {}".format(player+1))
    print("Your Hand")
    print("--------")
    count = 0
    for card in playerHand:
        print("# ", count, card)
        count = count + 1
    print("--------")
    print("")



def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #IP, port = target_server()
    IP, port = '127.0.0.1', 80
    client.connect((IP, port))

    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            message = message.split("*")
            # message[0] is the header
            # message[1] is the data
            #print(message)

            # send player name
            if message[0] == "gamename":
                threading.Thread(target=set_game_name, args=(client,)).start()
            # ready
            elif message[0] == "ready":
                # new thread for ready input
                threading.Thread(target=ready, args=(client, )).start()
            # receive cards
            elif message[0] == "card":
                show_card(message[1])
            #select and play a card

            elif message[0] == "selectedCard":
                play_card(message[1], client)
            # other message
            elif len(message[0]) != 0:
                print(message[0])
        except:
            client.close()
            break


main()











