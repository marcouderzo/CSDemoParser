# Worklog

This text file is used to keep track of the work being done so far.

## Downloading the Matches

### How?

Downloading the matches directly from Steam (e.g. calling Steam APIs) is not possible as far as we understand, as only CS:GO has the permission to download them. Another website, csgostats.gg, uses the Steam bootstrapper. Once you click on "View Demo" it launches CS:GO, redirects to the match page and downloads the demo. Unfortunately, CAPTCHAs prevent us to automate the download procedure, and going through CS:GO itself would not be very practical anyways.

After further investigation we found a stackoverflow [question](https://stackoverflow.com/questions/61859639/how-to-download-csgo-demo-from-match-sharing-code) about a similar use scenario. Quoting:

"Since 9/17/2019, Valve provided an API that allows players to give access to third-party websites to download their matchs history.
From this documentation, I have been able to get all my sharing code CSGO-xxxxx-xxxxx..., ready to download the matchs ! But, I didn't find any information about how to download them. In this page and the last one, we can read Third-party websites and applications can use this authentication code to access your match history, your overall performance in those matches, download replays of your matches, and analyze your gameplay. and This page outlines the basics of creating a website or application to access players match history and help with players statistics tracking and gameplay analysis."

### hltv.org

[hltv](https://hltv.org) is an extremely popular website  
This third-party website allows us to track down a specific player and retrieve all his previous matches. It is noteworthy that hltv.org downloads the match directly exactly like any other download without using any Steam Protocol or API whatsoever, so it looks like it is a much easier alternative. 

## The Parser: demoinfogo

### Why we chose it

[demoinfogo](https://github.com/ValveSoftware/csgo-demoinfo) is the official CS:GO opensource parser developed by Valve Software written in C/C++.

### Building demoinfogo on Windows

In order to build demoinfogo on Windows, follow these steps:

1. Download [protobuf-2.5.0.zip](https://github.com/google/protobuf/releases/download/v2.5.0/protobuf-2.5.0.zip) and extract it into the `parser` folder. This creates the folder `parser/protobuf-2.5.0`.
2. Download the Protobuf compiler [protoc-2.5.0.zip](https://github.com/google/protobuf/releases/download/v2.5.0/protoc-2.5.0-win32.zip) and extract it into the `parser/protoc-2.5.0-win32` folder.
3. Open `parser/protobuf-2.5.0/vsprojects/protobuf.sln` in Microsoft Visual Studio 2017. Allow Visual Studio to convert the projects.
4. Build the *Release* configuration of `libprotobuf`. Building any other projects is not required.
5. Open `parser/demoinfogo.vcxproj` in Microsoft Visual Studio 2017. Building the Release configuration creates the binary `parser/demoinfogo.exe`

## Automating the Parsing of the Match Pool

### autoparse.py

As the match pool is very large, parsing every match manually is just not feasable.
So, given the folder where all `.dem` matches are saved, the script will call a shell command for each match, telling demoinfogo to parse it. The `.txt` log file will be saved in `parser/logs` folder.
If any of the subprocesses return an exit code different than `1`, which is the default exit code of demoinfogo, then that means the parsing was not successful, and after finishing to parse all the match pool, you will find the failed match name listed in the report.
To setup the script, make sure you edit `demospath` in the source code to match your own demo folder. Then run the script with `python3 autoparse.py`.
