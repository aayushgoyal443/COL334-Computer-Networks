import socket
import select
import sys
import threading
import time

# Constants
MAX_CLIENTS = 10
SERVER_NAME = 'assyush'


def handle_chatting(conn, addr, s_name):
    while True:
        message = input(str("Me : "))
        if message == "[e]":
            message = "Left chat room!"
            conn.send(message.encode())
            print("\n")
            break
        conn.send(message.encode())
        message = conn.recv(1024)
        message = message.decode()
        print(s_name, ":", message)

def main():
    print("\nWelcome to Chat Room\n")
    time.sleep(1)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # this will form a TCP socket
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    host = socket.gethostname()
    ip = socket.gethostbyname(host)     # this is the IP address of our Server, client must pass this as server address in order to connect
    port = 1234     # this should be free
    server.bind((host, port))
    print(host, "(", ip, ")\n")
    server.listen(MAX_CLIENTS)

    clients = []    # each of them will be a pair, containing both the SEND and RECV sockets


    print("\nWaiting for incoming connections...\n")

    threads = []

    while True:
        conn, addr = server.accept()
        print("Received connection from ", addr[0], "(", addr[1], ")\n")

        s_name = conn.recv(1024)
        s_name = s_name.decode()
        conn.send(SERVER_NAME.encode())
        print(s_name, "has connected to the chat room\nEnter [e] to exit chat room\n")

        # Now i think it is the time to chat with them on a separate thread
        t = threading.Thread(target= handle_chatting , args= [conn, addr, s_name])  
        t.start()
        threads.append(t)
        

if __name__ == '__main__':
    main()
