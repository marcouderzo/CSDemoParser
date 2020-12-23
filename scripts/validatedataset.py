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

print("------REPORT-------")
if not isOutputClean:
    print("The following logs are not clean:")
    print(failedLogs)
    print("Bad Lines:")
    print(badLines)
else:
    print("All Logs Passed revision.")
            
