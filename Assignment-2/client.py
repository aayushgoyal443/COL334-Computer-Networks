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

def content_length(msg):
    return len(msg)


def disconnect():
    clientRECV.close()
    clientSEND.close()
    global connected
    connected = False


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

def valid_msg_format(msg):
    valid = True
    if (len(msg)<4):
        valid = False
    elif (msg[0]!= '@'):
        valid = False
    elif (msg[1] == ' '):
        valid = False
    if (valid):
        for (i,c) in enumerate(msg):
            if (c ==' ' and i< len(msg)-1 and msg[i+1]!= ' '):
                return True
    print('chat app: invalid message format')
    return False


def parse_message(msg):
    idx = -1
    for (i,c) in enumerate(msg):
        if (c ==' '):
            idx  = i
            break
    recipient =  msg[1:idx]
    message = msg[idx+1:]     # this will give us the username by removing the @ from it
    return recipient, message


def handle_send_feedback(feedback):
    if (feedback[0] == "SENT"):
        return True
    
    # We encountered some error 
    if (feedback[0] == "ERROR"):
        if (feedback[1] == "102"):
            print("server: Recipient is not registered")
            return True
        elif (feedback[1] == '103'):
            print('server: Header incomplete')
            return False


def send_messages():
    while connected:
        inp = input()
        inp  = inp.strip()      # for cleaning irrelevant newlines at start and end of message
        if (not valid_msg_format(inp)):
            continue
        recipient, msg =  parse_message(inp)
        message = f"SEND {recipient}\nContent-length: {content_length(msg)}\n\n{msg}"
        clientSEND.send(message.encode())
        #Now waiting for a response

        feedback = clientSEND.recv(MAX_MESSAGE_SIZE)
        feedback = feedback.decode().split()
        keep_running = handle_send_feedback(feedback)
        if (not keep_running):
            disconnect()


def is_well_formed(info):
    # check if ERROR 103 needs to be raised or not
    invalid = False
    if (len(info)!= 4):
        invalid = True
    elif (info[2] != ''):
        invalid = True
    else:
        header_info  = info[1].split(': ')
        if (len(header_info) != 2):
            invalid = True
        elif (header_info[0]!= "Content-length"):
            invalid = True
        elif ( len(info[3]) != int(header_info[1])):
            invalid = True

    return (not invalid)

def recv_messages():
    while connected:
        info = clientRECV.recv(MAX_MESSAGE_SIZE)
        info = info.decode().split('\n')
        if (not is_well_formed(info)):
            fd = f"ERROR 103 Header Incomplete\n\n"
            print("Incomplete header from server")
            clientRECV.send(fd.encode())
            disconnect()
        else:
            sender = info[0].split()[1]
            fd = f"RECEIVED {info}\n\n"
            clientRECV.send(fd.encode())
            print(f"{sender}: {info[3]}")


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
    global clientSEND, clientRECV

    #Opening the Receive socket
    clientRECV = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientRECV.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("\nTrying to connect RECV socket to ", host, "(", port, ")\n")
    try:
        clientRECV.connect((host, port))
    except:
        print("Not able to connect to server...try again")
    print(clientRECV)
    # Registering the RECV socket
    message = "REGISTER TORECV " + str(username) + "\n\n"
    clientRECV.send(message.encode())
    feedback = clientRECV.recv(MAX_MESSAGE_SIZE)
    feedback = feedback.decode().split()
    registered_receiver = handle_reg_feedback(feedback, clientRECV)

    #Opening the send socket
    clientSEND = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSEND.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("\nTrying to connect SEND socket to",  host +"#" + str(port))
    try:
        clientSEND.connect((host, port))
    except:
        print("Not able to connect to server...try again")
    # Registering the SEND socket
    message = f"REGISTER TOSEND {username} \n\n"
    clientSEND.send(message.encode())
    feedback = clientSEND.recv(MAX_MESSAGE_SIZE)
    feedback = feedback.decode().split()
    registered_sender = handle_reg_feedback(feedback, clientSEND)

    global connected
    connected = registered_sender and registered_receiver
    if (connected):
        print("\n------------------- Welcome to chatroom -------------------\n")


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