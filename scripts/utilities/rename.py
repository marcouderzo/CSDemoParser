import os

demospath = "F:/progetto/dem/"

print("the only purpose of this script is to batch-rename demo names if needed.")
print("player name: ")
playername = str(input())

i=1
for dem in os.listdir(demospath):
    name = playername + "_" + str(i) + ".dem"
    os.rename(demospath+dem, demospath+name)
    i=i+1