import os, subprocess

# Paste your own demo folder
targetpath = "F:/SteamLibrary/steamapps/common/Counter-Strike Global Offensive/csgo/replays"

hadErrors = False
failedParsings=[]

for file in os.listdir(targetpath):
    if file.endswith(".dem"):
        print("Parsing " + file)
        targetfile = os.path.join(targetpath, file).replace("\\", "/")
        p = subprocess.run(["C:/Users/marco/OneDrive/Marco/UniPD/Triennale/CyberSecurity/Progetto/csgo-demoinfo-master/parser/demoinfogo", targetfile], capture_output=True)
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