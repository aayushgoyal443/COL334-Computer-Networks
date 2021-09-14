from server import handle_chatting
import socket
import select
import sys
import threading
import time

# Desktop/COL334-Computer-Networks/Assignment-2/

# Global variables
threads = []

def handle_chatting(client, s_name):

    while True:
        message = client.recv(1024)
        message = message.decode()
        print(s_name, ":", message)
        message = input(str("Me : "))
        if message == "[e]":
            message = "Left chat room!"
            client.send(message.encode())
            print("\n")
            break
        client.send(message.encode())


def main():

    print("\nWelcome to Chat Room\n")
    print("Initialising....\n")
    time.sleep(1)

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        name = sys.argv[1]
    except:
        print("please pass username as command line argument")
        exit()

    host = input(str("Enter server address: ")) 
    port = 1234     # port of server
    print("\nTrying to connect to ", host, "(", port, ")\n")

    time.sleep(1)

    try:
        client.connect((host, port))
        print("Connected...\n")
    except:
        print("Not able to connect...try again :)")
        exit()

    client.send(name.encode())
    s_name = client.recv(1024)
    s_name = s_name.decode()
    print(s_name, "has joined the chat room\nEnter [e] to exit chat room\n")

    t=  threading.Thread(target= handle_chatting, args = [client, s_name])
    threads.append(t)
    t.start()


if __name__ == "__main__":
    main()