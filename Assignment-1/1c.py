import subprocess

domain_google = 'www.google.com'
domain_facebook = "www.facebook.com"
domain_iitd  = "www.iitd.ac.in"
low =1
high = 1<<32

#doing binary search to find the maximum packet size that we can send using ping command
while (low<=high):
    print(low, high)
    size = low + (high - low)//2
    out = subprocess.Popen(['ping', '-c', '1' , '-s', str(size) , domain_google], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT)
    stdout,stderr = out.communicate()
    stdout = str(stdout)
    if (stdout.find("option value too big")!=-1):
        high = size-1
    else:
        ans = size
        low = size +1

print(ans)

# Note: The maximum packet size that we can send will be same for all of them