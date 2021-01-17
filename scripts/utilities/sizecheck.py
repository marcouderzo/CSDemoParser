import os

logspath = "F:/progetto/log/"
demospath = "F:/progetto/dem/"

print("This script has the only purpose of running a quick check on log sizes to detect possible currupted logs.")
print("minimum size (kB:)")
threshold = int(input())

for log in os.listdir(logspath):
    lsize = (os.stat(logspath+log).st_size)/1000
    if  lsize < threshold: # kB 
        print(log + " : " + str(int(lsize))+" kB")

