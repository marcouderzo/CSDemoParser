# autoparse.py Script Documentation

## How does it work?

### Normalizing the Path

First of all, as we use a for `file in os.listdir(demospath)` loop to iterate through the matches, we decided to play it safe and normalize the path before passing it to the parser.
This is to say that every backslash is replaced with a forward slash, in order to avoid any issues with C++. Indeed, the latter uses backslashes as a line continuation character, corrupting the correct path and causing demoinfogo not to find the demo at all. 

### Calling demoinfogo

Given the folder where all `.dem` matches are saved, the script will call a shell command for each .dem match, telling demoinfogo to parse it. In detail:

`p = subprocess.run(["demoinfogo", "-gameevents", "-extrainfo", "-nofootsteps", "-nowarmup", "-packetentities", "-netmessages", demofile])`

The `.txt` log file will be saved in `parser/logs` folder.

### Handling Errors

If any of the subprocesses return an exit code different than `1`, (default exit code of demoinfogo), then it means the parsing was not successful. After finishing the parsing of all the match pool, you will find the failed match name listed in the report.


## Before you run the script

Make sure you edit `demospath` in the source code to match your own demo folder.
