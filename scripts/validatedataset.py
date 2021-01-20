# Output Validation Testing
# Checks for abnormal lines in the logs.
# Outputs may have a void line before EOF. The script will not count that as a new line
# If two or more blank lines are present, (\n), the script will consider such carriage return as new lines.

import os

# --------Setup------------

demospath = "F:/progetto/log/"      # Folder where logs are saved

enableLenghtTest = True             # Enable Line Count Test
linesThreshold = 0            # Minimum number of lines in log

nPlayers=34                       # number of players you are validating at once

# -------------------------

print("Set Lines Threshold: ")
linesThreshold = int(input())

isOutputClean=True

zeroedLogs = []
contaminatedLogs = []
actionOrEntityMissingLogs = []
emptyLogs = []
tooBriefLogs = []

print("Do want to run Test 1 (Output Validation)? (y/n)")
runOutputTest = input()

print("Do want to run Test 2 (nMatches/Player Validation)? (y/n)")
runHundredMatchesTest = input()

print("Do want to run Test 3 (Duplicates)? (y/n)")
runDupTest = input()

if(runOutputTest == "y"):
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
                print(file + ": Log has less lines than the set threshold. ("+str(i)+" lines)")
                tooBriefLogs.append(file)

            if not hasEntities or not hasActions and i != 0:
                print(file + ": Missing Actions or Entities!")
                actionOrEntityMissingLogs.append(file)


if runHundredMatchesTest=="y":
    print("")
    print("Running Test 2: Checking for Minimum 100 Matches Each Player...")

    i=0
    enoughMatches = True
    for file in os.listdir(demospath):
        if "_100" in file:
            i=i+1

    if i<34:
        print("Not enough Matches for some players!")        
        enoughMatches = False
            


if runDupTest == 'y':
    print("")
    print("Running Test 3: Checking for Doubled Matches...")

    duplicates=[]

    checked=0

    for file1 in os.listdir(demospath):
        if file1.endswith(".txt"):
            f1size=os.stat(demospath+file1).st_size # Checking each line would have taken more than 300 years.
            for file2 in os.listdir(demospath):
                if file2.endswith(".txt") and file2 != file1:
                    f2size=os.stat(demospath+file2).st_size
                    if(f1size==f2size):
                        duplicates.append(file1)
                        print(file1 + " and " + file2 + " : Found a duplicate")
        checked=checked+1                
        print("Matches Validated: "+ str(checked))

            
print("")
print("------DATASET VALIDATION REPORT-------")

if runOutputTest=="y":
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

if runHundredMatchesTest=="y":
    if not enoughMatches:
        print("Not Enough Matches for some players.")
    else:
        print("All Players Passed Test 2.")    
    
if runDupTest == 'y':
    if duplicates:
        print("Duplicates: ", duplicates)
    else:
        print("All Logs Passed Test 3.")
