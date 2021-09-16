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

# alter this to check for ERROR 102
def content_length(msg):
    return len(msg)


# To handle the feedback from server after regitration
def handle_reg_feedback(feedback, sock):
    if (feedback[0] == "REGISTERED"):
        if (feedback[1]  =="TOSEND"):
            print("Server: Registered to SEND")
        elif (feedback[1] =="TORECV"):
            print("Server: Registered to RECV")
        return True
    else:
        if (feedback[1] =="100"):
            print("Server: ERROR 100 Malformed username")
            sock.close()
        else:
            print("Server: ERROR 101 No user registered")
        exit()

# Handle feedback from server after sending message
def handle_send_feedback(feedback):
    if (feedback[0] == "SENT"):
        return True
    
    # We encountered some error 
    if (feedback[0] == "ERROR"):
        if (feedback[1] == "102"):
            print("Server: ERROR 102 Unable to send")
            return True
        elif (feedback[1] == '103'):
            print('Server: ERROR 103 Header incomplete\n')
            print('chat app: sending disconnected, only receiving messages now\n')
            return False


# to check is the format of message typed is correct or not @[recipient] [message]
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


# Parse the message to get the recipient and message
def parse_message(msg):
    idx = -1
    for (i,c) in enumerate(msg):
        if (c ==' '):
            idx  = i
            break
    recipient =  msg[1:idx]
    message = msg[idx+1:]     # this will give us the username by removing the @ from it
    return recipient, message


# returns False if ERROR 103 is present
def check_error_103(info):
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


# this function controls the sending of messages, works with clientSEND socket
def send_messages():
    while True:
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
            clientSEND.close()
            return


# this function controls receiving of messages, works with clientRECV socket
def recv_messages():
    while True:
        info = clientRECV.recv(MAX_MESSAGE_SIZE)
        info = info.decode().split('\n')
        if (not check_error_103(info)):
            fd = f"ERROR 103 Header Incomplete\n\n"
            print("Raised ERROR 103: Header Incomplete\n")
            print("receiving disconnected, only sending messages now\n")
            clientRECV.send(fd.encode())
            clientRECV.close()
            return
        else:
            sender = info[0].split()[1]
            fd = f"RECEIVED {info}\n\n"
            clientRECV.send(fd.encode())
            print(f"{sender}: {info[3]}")


# To connect and register to the server
def connect_and_register(host, port, username):

    # Making two sockets for sending and receiving
    global clientSEND, clientRECV

    #Opening the Receive socket
    clientRECV = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientRECV.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("Trying to connect RECV socket to",  host +"#" + str(port))
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

    #Opening the send socket
    clientSEND = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSEND.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("Trying to connect SEND socket to",  host +"#" + str(port))
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

    return (registered_sender and registered_receiver)


def main():

    if (len(sys.argv) != 3 ):
        print("Provide username and server address as command line arguments")
        exit()
    global username
    username = sys.argv[1]

    # host = input(str("Enter server address: ")) 
    host = sys.argv[2]
    port = SERVER_PORT     # port of server

    
    if (connect_and_register(host, port, username)):
        print("\n------------------- Welcome to chatroom -------------------\n")
    else:
        return 

    # starting 2 threads
    threadSEND= threading.Thread(target= send_messages, args = [])
    threadRECV= threading.Thread(target= recv_messages, args = [])
    threadSEND.start()
    threadRECV.start()

    if (threadRECV.is_alive()):
        threadRECV.join()
    if (threadSEND.is_alive()):
        threadSEND.join()
    clientRECV.close()
    clientSEND.close()


if __name__ == "__main__":
    main()