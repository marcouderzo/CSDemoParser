# validatedataset Documentation

## How it works

This is a very simple script that runs two tests on the final dataset.

### Test 1: Checking for Clean Output

For each log, this test checks for the following common defects we noticed while parse-testing:

**Check 1: Missing Entity/Action in the whole log**

Check if Entities and Actions are present at least once in the log.

**Check 2: Contaminated Output**

For each line, check if there is either the word "Action" or "Entity".

**Check 3: Zeroed Output**

Check if the log does not contain too many 0.000000 0.000000 0.000000 0.000000 in Entity occurencies.

**Check 4: Empty Log**

Check if the line count is 0.

**Check 5: Low Line Count**

Check if the line count is too low.


### Test 2: Checking for Duplicate Matches

For each log, the scripts checks every log (exept itself), to see if there are matches with the same output, meaning two parsed matches were the same. This does not apply if the logs are empty.

This is very important to check because hltv lists every match a player attends, but when we download a match, we actually download an archive of two or three matches (depending on the outcome: 2-0, 2-1).
As this is not as straight-forward as we thought it would be, we decided to double check the whole dataset once we were done parsing.

This is for sure the test that will take the most time to complete, as its complexity is O(n<sup>2</sup>)
