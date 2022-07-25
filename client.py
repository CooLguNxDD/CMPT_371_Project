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

# send ready to server
def ready(client):
    ready_msg = str(input("Input \"ready\" if you are ready \n"))
    if ready_msg == "ready":
        try:
            client.send(ready_msg.encode())
        except Exception as e: print(e)
    return

# show card on hand
def show_card(message):
    cards = json.loads(message).get("cards")
    showHand(cards)
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
    print("")

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #IP, port = target_server()
    IP, port = '127.0.0.1', 80
    client.connect((IP, port))
    gamename = input("Enter a Game Name ")

    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            message = message.split("*")
            # message[0] is the header
            # message[1] is the data
            #print(message[0])

            # send player name
            if message[0] == "gamename":
                client.send(gamename.encode('utf-8'))
            # ready
            elif message[0] == "ready":
                # new thread for ready input
                threading.Thread(target=ready, args=(client, )).start()
            # receive cards
            elif message[0] == "card":
                show_card(message[1])
            # other message
            elif len(message[0]) != 0:
                print(message[0])
        except:
            client.close()
            break


main()











