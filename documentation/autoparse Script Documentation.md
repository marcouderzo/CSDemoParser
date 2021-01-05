# autoparse.py Script Documentation

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
Then, for each possible SteamID of the current player, it calls the parser as a subprocess:

```
 p = subprocess.run(["demoinfogo", SteamID , demofile])
```

### Handling Errors

If any of the subprocesses return an exit code different than `1`, (default exit code of demoinfogo), then it means the parsing was not successful.
If the exit code is `2`, then it means the parser could not find the passed SteamID in the match, so it retries with the next SteamID. If it fails with every SteamID, it will append that match to the list of the failed parsings. If some other exit code is returned, the script will treat is an unknown error and will consider the parsing failed.

After finishing the parsing of all the match pool, you will find the failed parsings listed in the report.


## Before you run the script

- Edit `demospath` in the source code to match your own demo folder.
- Make sure you have `MatchesDict.json` in the same folder of the script.
