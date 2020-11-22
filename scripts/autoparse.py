import os, subprocess

# Paste your own demo folder
demospath = "F:/SteamLibrary/steamapps/common/Counter-Strike Global Offensive/csgo/replays"

hadErrors = False
failedParsings=[]

os.chdir("..")
os.chdir("parser")

for file in os.listdir(demospath):
    if file.endswith(".dem"):
        print("Parsing " + file)
        demofile = os.path.join(demospath, file).replace("\\", "/")
        p = subprocess.run(["demoinfogo", demofile])
        if(p.returncode != 1):
            hadErrors = True
            failedParsings.append(file)
            print("Unexpected exit code ("+ str(p.returncode) +") Match Parsing Failed")
        else:
            print("Parsed.")
        


print("--------REPORT--------")
if(hadErrors):
    print("Could not parse these matches:")
    print(failedParsings)
else:
    print("Done parsing match pool. No errors occurred.")