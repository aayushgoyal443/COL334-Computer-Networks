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

def isRegistered(username):
    if (username in registered_receivers) and (username in registered_senders):
        return True
    else:
        return False

# conn.send(message.encode())
# message = message.decode()


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


def serve_client(conn, addr):
    while True:
        continue
    


def handle_client_reg(conn, addr):
    message = conn.recv(MAX_MESSAGE_SIZE)
    message = message.decode()
    task = message.split()
    fault = False
    username = task[2]
    if ( len(task)!=3 or ((task[0] != "REGISTER" or (task[1]!= "TOSEND"  and task[1]!= "TORECV" )) and (not isRegistered(username)))):
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
    print(f"{username} has registered in the server")

    if (task[1] == "TOSEND"):
        serve_client(conn, addr)
    else:
        print("RECV thread closed")


def main():

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # this will form a TCP socket
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    host = socket.gethostname()
    ip = socket.gethostbyname(host)     # this is the IP address of our Server, client must pass this as server address in order to connect
    port = SERVER_PORT     # this should be free
    server.bind((host, port))
    print(host, "(", ip, ")\n")
    server.listen(MAX_CLIENTS)

    print("\nWaiting for incoming connections...\n")

    while True:
        conn, addr = server.accept()
        print("Received connection from ", addr[0], "(", addr[1], ")\n")
        # Now i think it is the time to chat with them on a separate thread
        t = threading.Thread(target= handle_client_reg , args= [conn, addr])
        t.start()
    
    # for thread in threads:
    #     if (thread.is_alive()):
    #         thread.join()


if __name__ == '__main__':
    main()
