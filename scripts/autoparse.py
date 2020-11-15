import os, subprocess

targetpath = "F:/SteamLibrary/steamapps/common/Counter-Strike Global Offensive/csgo/replays"
hadErrors = False
failedParsings=[]

for file in os.listdir(targetpath):
    if file.endswith(".dem"):
        print("Parsing " + file)
        targetfile = os.path.join(targetpath, file).replace("\\", "/")
        cmd = ['demoinfogo', '', targetfile]
        p = subprocess.Popen(cmd)
        p.wait()
        print("Process Returned " + str(p.returncode))
        if(p.returncode == 1):
            hadErrors= True
            failedParsings.append(file)


print("Done parsing match pool!")
print("--------REPORT---------")
if(hadErrors):
    print("Could not parse these matches:")
    print(failedParsings)
else:
    print("No errors occurred. All matches have been parsed successfully!")            