import matplotlib.pyplot as plt
import numpy as np 
import sys
from os import listdir
from os.path import isfile, join
ques = int(sys.argv[1])
input_dir = f"Q{ques}/outputs/toplot/"
output_dir = f"Q{ques}/outputs/plots/"
onlyfiles = [join(input_dir,f) for f in listdir(input_dir) if isfile(join(input_dir, f))] 

for FILE_NAME in onlyfiles:
    print(FILE_NAME)
    A = np.genfromtxt(FILE_NAME,dtype =  None)
    time = []
    size = []

    for t in A:
        time.append(t[0])
        size.append(int(t[1]))

    plt.plot(time, size)
    plt.xlabel("Time (in s)")
    plt.ylabel("Congestion window size")
    FILE_NAME = FILE_NAME.strip(".cwnd").split('/')[-1]
    plt.title(FILE_NAME)
    plt.savefig(f"{output_dir}{FILE_NAME}.png")
    plt.close()