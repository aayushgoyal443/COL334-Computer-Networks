import sys
import subprocess

COUNT =3
domain_google = 'www.google.com'
domain_facebook = "www.facebook.com"
domain_iitd  = "www.iitd.ac.in"
low =1
high = 1<<32

#doing binary search to find the maximum packet size that we can send using ping command
while (low<=high):
    print(low, high)
    size = low + (high - low)//2
    out = subprocess.Popen(['ping', '-c', str(COUNT) , '-s', str(size) , sys.argv[1]], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT)
    stdout,stderr = out.communicate()
    stdout = str(stdout)
    if (stdout.find("option value too big")!=-1): 
        high = size-1
    elif (stdout.find("0 packets received")!=-1):
        high = size-1
    else:
        ans = size
        low = size +1

print("Maximum packet size:", ans)

# www.google.com  -> 1472
# www.facebook.com -> 1472
# www.iitd.ac.in -> 65399