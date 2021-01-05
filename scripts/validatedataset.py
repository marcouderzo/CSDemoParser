# Output Validation Testing
# Checks for abnormal lines in the logs.
# Outputs may have a void line before EOF. The script will not count that as a new line
# If two or more blank lines are present, (\n), the script will consider such carriage return as new lines.

import os

# Paste your own demo folder
demospath = "F:/progetto/log/"

isOutputClean=True
failedLogs=[]
badLines=[]

print("Running Test 1: Checking for Clean Output...")


for file in os.listdir(demospath):
    hasEntites = False
    hasActions = False
    if file.endswith(".txt"):
        file_read = open(demospath+file, 'r')
        lines_read = file_read.readlines() 
        i = 0
        for line in lines_read:
            i=i+1
            if "Entity" in line:
                hasEntities = True
                continue

            if "Action" in line:   
                hasActions = True
                continue

            if "Entity" not in line and "Action" not in line:
                print(file + ": A line is not right!")
                badLines.append(line)
                isOutputClean=False
                failedLogs.append(file)
                break

        if i == 0:
            print(file + ": Empty File!")
            failedLogs.append(file)
        elif i < 100000:
            print(file + ": Log has too few lines.")
            failedLogs.append(file)

        if not hasEntities or not hasActions and i != 0:
            print(file + ": Missing Actions or Entities!")
            failedLogs.append(file)
        


print("")
print("Running Test 2: Checking for Doubled Matches...")

isDatasetDuplicated = False
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
                    isDatasetDuplicated=False
                    print(file1 + " and " + file2 + " : Found a duplicate")



            
print("------DATASET VALIDATION REPORT-------")
if not isOutputClean:
    print("The following logs are not clean:")
    print(failedLogs)
    print("Bad Lines:")
    print(badLines)
else:
    print("All Logs Passed Test 1.")

if isDatasetDuplicated:
    print("Found a duplicate of the following logs:")
    print(duplicates)    
else:
    print("All Logs Passed Test 2.")