import matplotlib.pyplot as plt
import numpy as np 
import sys

FILE_NAME =  sys.argv[1]

A = np.genfromtxt(FILE_NAME,dtype =  None)
time = []
size = []

for t in A:
    time.append(t[0])
    size.append(int(t[1]))

time = np.array(time)
size = np.array(size)

plt.plot(time, size)
plt.xlabel("Time (in s)")
plt.ylabel("Congestion window size")

FILE_NAME = FILE_NAME.split('.')[0].split('/')[-1].split('_')[-1]

plt.title(FILE_NAME)

plt.savefig(f"plots/{FILE_NAME}")