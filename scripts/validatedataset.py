# Output Validation Testing
# Checks for abnormal lines in the logs.
# Outputs may have a void line before EOF. The script will not count that as a new line
# If two or more blank lines are present, (\n), the script will consider such carriage return as new lines.

import os

# Paste your own demo folder
demospath = "C:/Users/marco/Desktop/ParserTests/auto/"

isOutputClean=True
failedLogs=[]
badLines=[]

print("Running Test 1: Checking for Clean Output...")

for file in os.listdir(demospath):
    if file.endswith(".txt"):
        file_read = open(demospath+file, 'r')
        lines_read = file_read.readlines() 
        for line in lines_read:
            if "Entity" not in line and "Action" not in line:
                badLines.append(line)
                isOutputClean=False
                failedLogs.append(file)
                break


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
                    duplicates.append(f1)
                    isDatasetDuplicated=False
                    #print("Found a duplicate: " + file1 + " and " + file2) #in case you want to check the two filenames



            
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