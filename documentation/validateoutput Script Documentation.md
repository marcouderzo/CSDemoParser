# validatedataset Documentation

## How it works

This is a very simple script that runs two tests on the final dataset.

### Test 1: Checking for Clean Output

For each log, the script checks every line, to see if there is either the word "Action" or "Entity". If that's not the case, it means that something in the parsing process went wrong.

### Test 1: Checking for Duplicate Matches

For each log, the scripts checks every log (exept itself), to see if there are matches with the same output, meaning two parsed matches were the same. This is very important to check because hltv lists every match a player attends, but when we download a match, we actually download an archive of two or three matches (depending on the outcome: 2-0, 2-1).
As this is not as straight-forward as we thought it would be, we decided to double check the whole dataset once we were done parsing.
