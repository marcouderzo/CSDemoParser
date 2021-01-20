# validatedataset Documentation

## How it works

This is a very simple script that runs two tests on the final dataset.

### Test 1: Checking for Clean Output

For each log, this test checks for the following common defects we noticed while parse-testing:

- **Check 1: Missing Entity/Action in the whole log**

Check if Entities and Actions are present at least once in the log.

- **Check 2: Contaminated Output**

For each line, check if there is either the word "Action" or "Entity".

- **Check 3: Zeroed Output**

Check if the log does not contain too many 0.000000 0.000000 0.000000 0.000000 in Entity occurencies.

- **Check 4: Empty Log**

Check if the line count is 0.

- **Check 5: Low Line Count**

Check if the line count is too low.


### Test 2: Checking if there are 100 matches for each player

Searches for "100" in the filename for n times, with n = number of players in the target folder.

### Test 3: Checking for Duplicate Matches

For each log, the scripts checks every log size (exept itself), to see if there are matches with the same output, meaning two parsed matches were the same.

This is very important to check because hltv lists every match a player attends, but when we download a match, we actually download an archive of two or three matches (depending on the outcome: 2-0, 2-1).
As this is not as straight-forward as we thought it would be, we decided to double check the whole dataset once we were done parsing.

Our original idea was to check each line of each file, but as the complexity of the algorithm was O(n<sup>2</sup>), it would have taken more than three hundred years to complete. Therefore, we switched to only checking the file size in bytes.
