import sys
import time
import socket
import struct

# Constants
MAX_HOPS = 64
ICMP_CODE = socket.getprotobyname('icmp')
PACKET_COUNT =1
RETRIES=5
ICMP_ECHO_REQUEST = 8 

def checksum(packet):
    sum=0
    n = len(packet)
    for i in range(0, n, 2):
        sum += packet[i] + (packet[i+1]<<8)
        sum  = (sum & 0xffff) + (sum >>16)
    sum  = socket.htons(~sum & 0xffff)
    return sum

try:
    dest_addr = sys.argv[1]
except:
    print("Provide domain name as command line argument")
    exit()

print("Going to traceroute the address", dest_addr)
sock_formed = False
for t in range (RETRIES):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, ICMP_CODE)  # root priveldge is required for forming socket
        sock_formed = True
        break
    except:
        print("Not able to form the socket, try:", t+1 )

if (sock_formed):
    my_socket = sock
    my_socket.settimeout(1)
    print("Socket formed")
else:
    print("Not able to form the socket")
    exit()

for ttl in range (1,MAX_HOPS+1):
    
    # We will ping the dest_addr using the socket formed above with varying ttl values

    try:
        my_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
    except:
        print("Not able to update the ttl value:", ttl)
        continue
    
    # Forma packet with dummy information to be sent
    host_IP = socket.gethostbyname(dest_addr)

    # print(host_IP)

    header = struct.pack("!BBHHH", ICMP_ECHO_REQUEST, 0, 0, 0, 0)
    packet = struct.pack("!BBHHH", ICMP_ECHO_REQUEST, 0, checksum(header), 0, 0)

    for _ in range (PACKET_COUNT):
        try: 
            t= time.time()

            my_socket.sendto(packet, (host_IP, 1))
            resp,  (route_ip, _ )  = my_socket.recvfrom(1024)

            rtt  = (time.time() - t)*1000   # round trip time in seconds

            if (checksum(resp)!=0):
                raise socket.timeout

            print(route_ip, end  = "\t", flush  = True)
            print(rtt, flush  = True)
            
        except socket.timeout:
            print("*", flush  = True)
    
    if (route_ip == host_IP):
        break

    

    

    # we are getting the correct ip addresses of the routes, and a good enough rtt value. Now need to take care of the * thing