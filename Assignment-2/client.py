import socket
import select
import sys
import threading
import time

# Desktop/COL334-Computer-Networks/Assignment-2/

#Constants
SERVER_PORT = 1234
MAX_MESSAGE_SIZE = 1024

# Global variables


def handle_reg_feedback(feedback, sock):
    if (feedback[0] == "REGISTERED"):
        if (feedback[1]  =="TOSEND"):
            print("Registered to send")
        elif (feedback[1] =="TORECV"):
            print("Registered to recv")
        return True
    else:
        if (feedback[1] =="100"):
            print("Malformed username")
            sock.close()
        else:
            print("Server:", "No user registered")
        exit()

def send_messages():
    while True: 
        continue

def recv_messages():
    while True:
        continue


def main():

    if (len(sys.argv) != 3 ):
        print("Provide username and server address as command line arguments")
        exit()
    global username
    username = sys.argv[1]

    # host = input(str("Enter server address: ")) 
    host = sys.argv[2]
    port = SERVER_PORT     # port of server

    # Making two sockets for sending and receiving

    #Opening the send socket
    clientSEND = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSEND.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("\nTrying to connect SEND socket to",  host +"#" + str(port) + "\n")
    try:
        clientSEND.connect((host, port))
    except:
        print("Not able to connect to server...try again")
    # Registering the SEND socket
    message = "REGISTER TOSEND " +str(username) + "\n\n"
    clientSEND.send(message.encode())
    feedback = clientSEND.recv(MAX_MESSAGE_SIZE)
    feedback = feedback.decode().split()
    registered_sender = handle_reg_feedback(feedback, clientSEND)


    #Opening the Receive socket
    clientRECV = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientRECV.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("\nTrying to connect RECV socket to ", host, "(", port, ")\n")
    try:
        clientRECV.connect((host, port))
    except:
        print("Not able to connect to server...try again")
    # Registering the RECV socket
    message = "REGISTER TORECV " + str(username) + "\n\n"
    clientRECV.send(message.encode())
    feedback = clientRECV.recv(MAX_MESSAGE_SIZE)
    feedback = feedback.decode().split()
    registered_receiver = handle_reg_feedback(feedback, clientRECV)


    if (registered_sender and registered_receiver):
        print("\Welcome to chatroom\n")


    global threadSEND, threadRECV
    threadSEND= threading.Thread(target= send_messages, args = [])
    threadRECV= threading.Thread(target= recv_messages, args = [])
    threadSEND.start()
    threadRECV.start()

    if (threadSEND.is_alive()):
        threadSEND.join()
    if (threadRECV.is_alive()):
        threadRECV.join()


if __name__ == "__main__":
    main()