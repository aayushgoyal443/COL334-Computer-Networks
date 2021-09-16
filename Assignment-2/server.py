import socket
import select
import sys
import threading
import time

# Constants
MAX_CLIENTS = 16
SERVER_PORT = 1234
MAX_MESSAGE_SIZE = 1024

# Global Variables
registered_senders = {}
registered_receivers = {}
feedbacks = []      # for storing feedbacks from broadcast, since threading can call only non-void functions

def content_length(msg):
    return len(msg)

def disconnect_user(username):
    if (username in registered_senders):
        registered_senders[username][0].close()
        registered_senders.pop(username)
    if (username in registered_receivers):
        registered_receivers[username][0].close()
        registered_receivers.pop(username)


def is_registered(username):
    if username not in registered_receivers:
        return False
    if username not in registered_senders:
        return False
    return True


# To check if a username if valid or not
def valid_username(username):
    for c in username:
        if ( 'a' <= c <= 'z'): 
            continue
        elif ('A' <= c <= 'Z'):
            continue
        elif ('0' <= c <= '9'):
            continue
        else:
            return False
    return True

def broadcast(sender, msg):
    global feedbacks
    feedbacks = []
    ts = []
    i=0
    for recipient in registered_receivers:
        if (recipient == sender):
            continue
        feedbacks.append("")
        t = threading.Thread(target= unicast, args = [recipient, sender,  msg, i])
        t.start()
        ts.append(t)
        i+=1

    for t in ts:
        t.join()
    for fd in feedbacks: 
        if (fd == "ERROR 102 Unable to send\n\n"):
            return fd
    return "SENT ALL"
    

def unicast(recipient, sender, msg, idx =-1):
    if (recipient not in registered_receivers):
        feedback = "ERROR 102 Unable to send\n\n"
        return feedback
    # The recipent is registered and hence we should send them message
    message = f"FORWARD {sender}\nContent-length: {content_length(msg)}\n\n{msg}"
    registered_receivers[recipient][0].send(message.encode())
    feedback = registered_receivers[recipient][0].recv(MAX_MESSAGE_SIZE)
    feedback = feedback.decode().split()
    if (feedback[0] == "ERROR" and feedback[1] == "103"):
        disconnect_user(recipient)
        fd = "ERROR 102 Unable to send\n\n"
    else: 
        # it would have got the "RECEIVED"
        fd = "SENT {recipient}\n\n"
    if (idx!=-1):
        feedbacks[idx] = fd
    return fd


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


def serve_client(conn, addr, username):
    while is_registered(username):
        message= conn.recv(MAX_MESSAGE_SIZE)
        info = message.decode().split('\n')
        if not is_well_formed(info):
            feedback = f"ERROR 103 Header incomplete\n\n"
            conn.send(feedback.encode())
            disconnect_user(username)
            continue
        recipient = info[0].split()[1]
        if (recipient == "ALL"):
            feedback = broadcast(username, info[3])
        else:
            feedback = unicast(recipient,username, info[3])
        feedback= feedback.split()
        if (feedback[0] == 'SENT'):
            feedback  = f"SENT {recipient}"
        else:
            feedback = f"ERROR 102 Unable to send"
        
        conn.send(feedback.encode())

def handle_client_reg(conn, addr):
    message = conn.recv(MAX_MESSAGE_SIZE)
    task = message.decode().split()
    fault = False
    username = task[2]
    if ( len(task)!=3 or ((task[0] != "REGISTER" or (task[1]!= "TOSEND"  and task[1]!= "TORECV" )) and (not is_registered(username)))):
        feedback = f"ERROR 101 No user registered\n\n"
        fault = True
    if ( (not fault) and (not valid_username(username)) ):
        feedback =  f'ERROR 100 Malformed username\n\n'
        fault = True
    
    if (fault):
        conn.send(feedback.encode())
        conn.close()
        return

    # All good, no fault
    if (task[1] == "TORECV"):
        registered_receivers[username] = (conn, addr)
        feedback = 'REGISTERED TORECV '+ str(username) + '\n\n'
    else:
        registered_senders[username] = (conn, addr)
        feedback = 'REGISTERED TOSEND '+ str(username) + '\n\n'
    conn.send(feedback.encode())
    print(feedback.strip() + str("\n"))

    if (task[1] == "TOSEND"):
        serve_client(conn, addr, username)


def main():

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # this will form a TCP socket
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    host = socket.gethostname()
    ip = socket.gethostbyname(host)     # this is the IP address of our Server, client must pass this as server address in order to connect
    port = SERVER_PORT     # this should be free
    server.bind((host, port))
    print(host, "(", ip, ")")
    server.listen(MAX_CLIENTS)

    print("\nWaiting for incoming connections...\n")

    while True:
        conn, addr = server.accept()
        print(f"Received connection from {addr[0]}#{addr[1]}")
        # Now i think it is the time to chat with them on a separate thread
        t = threading.Thread(target= handle_client_reg , args= [conn, addr])
        t.start()
    
    # for thread in threads:
    #     if (thread.is_alive()):
    #         thread.join()


if __name__ == '__main__':
    main()
