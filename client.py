import socket

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

client.connect(('127.0.0.1',80))
gamename = input("Enter a Gamename ")



while True:
    try:
        message = client.recv(1024).decode('utf-8')
        if message == 'gamename':
            client.send(gamename.encode('utf-8'))
        elif len(message) != 0 :
            print(message)
    except:
        client.close()
        break



