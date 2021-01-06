# autoparse.py Script Documentation


## Setup

- In demoinfogo, make sure you edit the output folder in `demoinfogo.cpp`. (e.g. `file = "F:/progetto/log/" + file + ".txt";`)
- Edit `demospath` in the source code to match your own demo folder.
- Edit `logpath` in the source code to match your own logs folder. (To be read from)
- Make sure you have `MatchesDict.json` in the same folder of the script, else specify the path.
- Edit `lineThreshold` to set the minimum number of lines the script expects logs to have, in case it checks it.

## How does it work?

### Normalizing the Path

When working with paths, every backslash is replaced with a forward slash, in order to avoid any issues with C++. Indeed, the latter uses backslashes as a line continuation character, corrupting the correct path and causing demoinfogo not to find the demo at all. 

### Dictionaries

The script uses two dictionaries:

**SteamID Dictionary**

`SteamID_dict` is a Python dictionary that contains all the SteamIDs of the players. It is defined inside the script as it is completely static and predetermined. 

**Matches Dictionary**

`MatchesDict` is a Python dictionary that contains all the matches, organized by players. Is is loaded from a `.json` file created by the `autodownload.py` script.

### Iterating through the Matches and Calling demoinfogo

For each player in the `MatchesDict` dictionary, the scripts iterates through the list of matches and searches the corresponding match in the demos folder. 
Then, for each possible SteamID of the current player, it calls the parser as a subprocess, until the parsing is successful:

```
 p = subprocess.run(["demoinfogo", SteamID , demofile])
```

### Handling Return Codes

**Return Code 1**

Default exit code, meaning the parsing process was successful.

**Return Code 2**

If the exit code is `2`, then it means the parser could not find the passed SteamID in the match, so it retries with the next SteamID.

**Return Code 3**

A few demos here and there exit with code 3 (Fatal Error from the parser, probably due to some corruption at the end of the demo), though the parsing process is completed anyways. Even though we consider the parsing successful, we still play it safe and append it to a list for further inspection.

**Return Code 3221226505**

Some demos cause a Stack Overflow in the parser while dumping the very last packet of the demo. The parsing is still successful, but this error truncates the last line of the log. Therefore, we open the log file and erase the truncated line. We then check the line count in order to assess whether or not it is reasonable to assume the log is complete. If it is not, we append the file to a list of matches with low line count for further inspection.
If all of this goes well, we consider the parsing successful. We still append the file to a list of matches that need a check.

### Report

At the end of the process, a Report is dumped.
