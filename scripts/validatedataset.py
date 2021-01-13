# Output Validation Testing
# Checks for abnormal lines in the logs.
# Outputs may have a void line before EOF. The script will not count that as a new line
# If two or more blank lines are present, (\n), the script will consider such carriage return as new lines.

import os

# --------Setup------------

demospath = "F:/progetto/log/"      # Folder where logs are saved

enableLenghtTest = True             # Enable Line Count Test
linesThreshold = 70000            # Minimum number of lines in log

nPlayers=50                         # number of players you are validating at once

# -------------------------



isOutputClean=True

zeroedLogs = []
contaminatedLogs = []
actionOrEntityMissingLogs = []
emptyLogs = []
tooBriefLogs = []


print("Do you also want to run Test 3 (Duplicates)? This will take a long time to complete. (y/n)")
runDupTest = input()


print("Running Test 1: Checking for Clean Output...")


for file in os.listdir(demospath):
    hasEntites = False
    hasActions = False
    if file.endswith(".txt"):
        file_read = open(demospath+file, 'r')
        lines_read = file_read.readlines() 
        i = 0
        nullCounter = 0
        for line in lines_read:
            i=i+1
            if line.find("0.000000 0.000000 0.000000 0.000000")!=-1:
                nullCounter +=1
                
            if "Entity" in line:
                hasEntities = True
                continue

            if "Action" in line:   
                hasActions = True
                continue

            if "Entity" not in line and "Action" not in line:
                print(file + ": A line does not contain Entity/Action! Line: "+ line)
                contaminatedLogs.append(file)
                break

        if(nullCounter > i-(i/3)):
            print(file + ": Too many null lines (" + str(nullCounter) + "/" + str(i) +" lines)")
            zeroedLogs.append(file)

        if i == 0:
            print(file + ": Empty File!")
            emptyLogs.append(file)
        elif i < linesThreshold and enableLenghtTest:
            print(file + ": Log has too few lines.")
            tooBriefLogs.append(file)

        if not hasEntities or not hasActions and i != 0:
            print(file + ": Missing Actions or Entities!")
            actionOrEntityMissingLogs.append(file)


print("")
print("Running Test 2: Checking for Minimum 100 Matches Each Player...")

i=0
enoughMatches = True
for file in os.listdir(demospath):
    if "_100" in file:
        i=i+1

if i<20:
    print("Not enough Matches for some players!")        
    enoughMatches = False
            

if runDupTest == 'y':
    print("")
    print("Running Test 3: Checking for Doubled Matches...")

    duplicates=[]

    for file1 in os.listdir(demospath):
        if file1.endswith(".txt"):
            f1 = open(demospath+file1)
            for file2 in os.listdir(demospath):
                if file2.endswith(".txt") and file2 != file1:
                    f2 = open(demospath+file1)
                    if f1.read() == f2.read():
                        lines_read = f1.readlines()
                        i = 0
                        for line in lines_read:
                            i=i+1
                        if i == 0:
                            continue    
                        duplicates.append(f1)
                        print(file1 + " and " + file2 + " : Found a duplicate")

            

print("------DATASET VALIDATION REPORT-------")

if zeroedLogs:
    print("Logs With Too Many Zeros: ", zeroedLogs)
if contaminatedLogs:
    print("Contaminated Logs: ", contaminatedLogs)
if actionOrEntityMissingLogs:
    print("Logs Missing Actions or Entities: ", actionOrEntityMissingLogs)
if emptyLogs:
    print("Empty Logs: ", emptyLogs)
if tooBriefLogs:
    print("Too Brief Logs", tooBriefLogs)
else:
    print("All Logs Passed Test 1.")

if not enoughMatches:
    print("Not Enough Matches for some players.")
else:
    print("All Players Passed Test 2.")    
    
if runDupTest == 'y':
    if duplicates:
        print("Duplicates: ", duplicates)
    else:
        print("All Logs Passed Test 3.")
