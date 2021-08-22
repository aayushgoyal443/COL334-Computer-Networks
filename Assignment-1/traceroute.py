import sys
import time
import socket
import struct
import matplotlib.pyplot as plt

# Constants
MAX_HOPS = 64
PACKET_COUNT =3
RETRIES=5
ICMP_ECHO_REQUEST = 8
TIMEOUT = 2 

def checksum(packet):
    sum=0
    n = len(packet)
    for i in range(0, n, 2):
        sum += packet[i] + (packet[i+1]<<8)
        sum  = (sum & 0xffff) + (sum >>16)
    sum  = socket.htons(~sum & 0xffff)
    return sum

# Reading domain name from command line
try:
    dest_addr = sys.argv[1]
except:
    print("Provide domain name as command line argument")
    exit()

host_IP = socket.gethostbyname(dest_addr)   # getting the route IP address of domain name, just like nslookup

# Forming a ICMP server socket, remember to give root permissions
print('\ntraceroute to ' + dest_addr + ' (' + str(host_IP) +  '), '+ str(MAX_HOPS) + ' hops max\n')
sock_formed = False
for t in range (RETRIES):
    try:
        my_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)  # root priveldge is required for forming socket
        my_socket.settimeout(TIMEOUT)
        sock_formed = True
        # print("Socket formed")
        break
    except:
        print("Not able to form the socket, try:", t+1 )

if (sock_formed == False):
    print("Not able to form the socket")
    exit()

# Varying the ttl value to get the IP addresses hop by hop
# We will ping the dest_addr using the socket formed above with varying ttl values

x = []  # this will store the hop number
y = []  # this will store the rtt value for that hop

for ttl in range (1,MAX_HOPS+1):

    print(ttl, end = "    ")
    x.append(ttl)
    try:
        my_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)     # Updating the ttl value of socket
    except:
        print("Not able to update to ttl value:", ttl)
        continue

    # Forming an empty packet
    header = struct.pack("!BBHHH", ICMP_ECHO_REQUEST, 0, 0, 0, 0)
    packet = struct.pack("!BBHHH", ICMP_ECHO_REQUEST, 0, checksum(header), 0, 0)

    rtts = []
    route_ip = ""

    for _ in range (PACKET_COUNT):
        try: 
            t= time.time()

            my_socket.sendto(packet, (host_IP, 1))
            resp,  (ip, _ )  = my_socket.recvfrom(1024)

            rtt  = (time.time() - t)*1000   # round trip time in seconds

            if (checksum(resp)!=0):
                raise socket.timeout

            rtts.append(rtt)
            if (ip != ""):
                route_ip = ip
            
        except socket.timeout:
            rtts.append("*")

    if (route_ip != ""):
        print(route_ip, end = "\t")

    least =0 
    for rtt in rtts:
        if rtt == "*":
            print("*", end = "  ")
        else:
            print('%.3f'%rtt + 'ms', end = "  ")
            if (least ==0):
                least  = rtt
            else:
                least = min(least, rtt)
    y.append(least)

    print()
    if (route_ip == host_IP):
        break

# Plot the graph using x and y

plt.plot(x, y)
plt.xlabel('Hop number')
plt.ylabel('Round trip time (in ms)')
plt.title('Hop number v/s rtt values')
plt.savefig( "plots/" + str(dest_addr)+".png")
plt.close("all")