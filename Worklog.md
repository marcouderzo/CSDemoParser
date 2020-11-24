# Worklog

This text file is used to keep track of the work being done so far.

## Downloading the Matches

### Finding Matches

In order to populate the match pool, we need 50 players and 100 matches for each of them. Using Steam APIs was not possible. 
Although since 9/17/2019, Valve provided an [API](https://developer.valvesoftware.com/wiki/Counter-Strike:_Global_Offensive_Access_Match_History) that allows players to give access to third-party websites to download their matchs history, not every user can get those informations. Indeed, the [documentation](https://developer.valvesoftware.com/wiki/Counter-Strike:_Global_Offensive_Access_Match_History) states that to do that you would need a Game Authentication Code created by the user, together with one of their match sharing codes. So, unless you make them log-in through the Steam API and ask them to partecipate to the project, this path doesn't lead anywhere.
So we had to look on third-party websites that already use this method. [csgostats.gg](https://csgostats.gg) is a website where you can find all the matches played, check for specific players (Pros and generic players also), and watch their demos. As you click the Watch Demo link, it will launch the Steam Bootstrapper and will start up CS:GO and download the match locally. We suppose that is done through the Steam Protocol with: `steam://rungame/730/:steamID:/+csgo_download_match%20CSGO-xxxxx-xxxxx`  Unfortunately, csgostats has CAPTCHAS that just make the automation of the procedure very tricky, maybe not even possible.

### Where are CS:GO matches saved and How are they shared?

Demos are saved on Valve's servers and are downloadable from a link in the form of `http://replay131.valve.net/730/xxxxxxxxxxxxxxxxxxxxx_xxxxxxxxx.dem.bz2`, where "x" is the MatchID, OutcomeID and TokenID. Those links, as well as the three parameters we just mentioned, are not publically available online, not even on third-party websites. So we needed a way to either get the link from the match list of a player or reconstruct it.
[node-csgo](https://github.com/joshuaferrara/node-csgo) is a really powerful plugin for CS:GO, also used by csgostats.gg to get the matches. Note that even csgostats uses the API introduced with the 9/17/2019 CS:GO update.
What we needed to do was not in the cards for node-csgo, but it is still worth mentioning why. It is possible to retrieve the link in two ways:
- from the sharecode, using `CSGO.SharecodeDecoder(string code).decode();` That should return the MatchID, OutcomeID and TokenID needed to reconstruct the link.
Unfortunately, CS:GO sharecodes are made not to be public and cannot be retrieved in any way unless the player shares it with you or allows the third party website to retrieve it through the Steam API.
- directly, using `requestRecentGames()` : Requests a list of recent games for the currently logged in account. Listen for the `matchList` event for the game coordinator's response, where you will find the download link as: `"map":"http://replay124.valve.net/730/003072985384448163905_0699089210.dem.bz2"` . Although very convenient, as you wouldn't need any sharecode, that cannot be a solution because you would need to make the player log-in instead, which is clearly not feasable.

### Our Choice: hltv.org

So, the only way we could retrieve the matches was through third-party websites only. 
[hltv](https://hltv.org) is an extremely popular website used to track Pro CS:GO Competitive Matches. It allows us to track down a specific player and retrieve all his previous matches. It is noteworthy that hltv.org downloads the match directly exactly like any other download without using any Steam Protocol or API whatsoever, so it looks like a much easier alternative.

### Web Scraping in Python

Write here.



## The Parser: demoinfogo

### Why we chose it

[demoinfogo](https://github.com/ValveSoftware/csgo-demoinfo) is the official CS:GO opensource parser developed by Valve Software written in C/C++. The fact that it comes from Valve itself is a compelling reason to use it, even though it doesn't really come with any documentation on how it works on a deeper level. 

### Building demoinfogo on Windows

In order to build demoinfogo on Windows, follow these steps:

1. Download [protobuf-2.5.0.zip](https://github.com/google/protobuf/releases/download/v2.5.0/protobuf-2.5.0.zip) and extract it into the `parser` folder. This creates the folder `parser/protobuf-2.5.0`.
2. Download the Protobuf compiler [protoc-2.5.0.zip](https://github.com/google/protobuf/releases/download/v2.5.0/protoc-2.5.0-win32.zip) and extract it into the `parser/protoc-2.5.0-win32` folder.
3. Open `parser/protobuf-2.5.0/vsprojects/protobuf.sln` in Microsoft Visual Studio 2017. Allow Visual Studio to convert the projects.
4. Build the *Release* configuration of `libprotobuf`. Building any other projects is not required.
5. Open `parser/demoinfogo.vcxproj` in Microsoft Visual Studio 2017. Building the Release configuration creates the binary `parser/demoinfogo.exe`

### Reverse Engineering the Parser and Modifying it to suit our needs

- First of all, demoinfogo doesn't natively output to a file, it just uses `printf()` functions to print the information to the console, preventing us to log the data and analyze it. This is why we figured out a very easy way of redirecting the output to a file using the [`freopen`](http://www.cplusplus.com/reference/cstdio/freopen/) C++ function. In demoinfogo.cpp you will find:

		freopen(file.c_str(), "w", stdout);
		DemoFileDump.DoDump();
		fclose(stdout);

Encapsulating the `DemoFileDump.DoDump()` call between freopen and fclose, without changing anything else in the source code of the parser, enabled us to log every match in a dedicated .txt file.

- Of course demoinfogo parses the whole match and gives too much information, the majority of which is not useful to us. As you can see in demoinfogo.cpp, the application is able to take in some optional arguments. Already, `-deathscsv`, `-stringtables`, `-datatables`, `-netmessages` are not useful to us. As of right now, `-gameevents -extrainfo -nofootsteps -nowarmup -packetentities` are the only useful optional arguments.
Then we analyzed the log of a parsed match and figured out where the not so useful printf() calls were coming from, in order to remove them and "declutter" the log.



## Automating the Parsing of the Match Pool

### autoparse.py

As the match pool is very large, parsing every match manually is just not feasable.
So, given the folder where all `.dem` matches are saved, the script will call a shell command for each match, telling demoinfogo to parse it. The `.txt` log file will be saved in `parser/logs` folder.
If any of the subprocesses return an exit code different than `1`, which is the default exit code of demoinfogo, then that means the parsing was not successful, and after finishing to parse all the match pool, you will find the failed match name listed in the report.
To setup the script, make sure you edit `demospath` in the source code to match your own demo folder. Then run the script with `python3 autoparse.py`.
