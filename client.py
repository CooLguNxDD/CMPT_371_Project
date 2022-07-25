import socket


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

def ready(client):
    ready_msg = str(input("Input \"ready\" if you are ready"))
    if ready_msg == "ready":
        try:
            client.send(ready_msg.encode())
        except Exception as e: print(e)
    return

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    IP, port = target_server()
    client.connect((IP, port))
    gamename = input("Enter a Game Name ")

    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'gamename':
                client.send(gamename.encode('utf-8'))
            elif message == 'ready':
                # trigger ready to server
                ready(client)
            elif len(message) != 0:
                print(message)
        except:
            client.close()
            break


main()











