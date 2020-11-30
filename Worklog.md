# Project Worklog

This text file is used to keep track of the work being done so far, as well as to give a detailed and exhausive explaination about what we have found out during the project and the reasonings behind our decisions.

Students Involved in the Project:
- [Marco Uderzo](https://github.com/marcouderzo)
- [Samuel Kostadinov](https://github.com/Neskelogth)

## Downloading the Matches

### Finding Matches

In order to populate the match pool, we need 50 players and 100 matches for each of them. Using Steam APIs was not possible. 
Although since 9/17/2019, Valve has provided an [API](https://developer.valvesoftware.com/wiki/Counter-Strike:_Global_Offensive_Access_Match_History) that allows players to give access to third-party websites to download their match history, not every user can get those information. Indeed, the [documentation](https://developer.valvesoftware.com/wiki/Counter-Strike:_Global_Offensive_Access_Match_History) states that to do it you would need a Game Authentication Code created by the user, together with one of their match sharing codes. So, unless you make them log-in through the Steam API and ask them to partecipate to the project, this path doesn't lead anywhere.

Therefore we had to look on third-party websites that already use this method. [Csgostats.gg](https://csgostats.gg) is a website where you can find all the matches played, check for players and watch their demos. 

As you click the Watch Demo link, the Steam Bootstrapper will be launched and CS:GO will be started up and the match will be downloaded locally. We suppose it is done through the Steam Protocol with: `steam://rungame/730/:steamID:/+csgo_download_match%20CSGO-xxxxx-xxxxx`  Unfortunately, csgostats has CAPTCHAS that just make the automation of the procedure very tricky, maybe not even possible.

### Where are CS:GO matches saved and How are they shared?

Demos are saved on Valve's servers and are downloadable from a link in the form of `http://replay131.valve.net/730/xxxxxxxxxxxxxxxxxxxxx_xxxxxxxxx.dem.bz2`, where "x" is the MatchID, OutcomeID and TokenID. Those links, as well as the three parameters we just mentioned, are not publically available online, not even on third-party websites. So we needed a way to either get the link from the match list of a player or reconstruct it.

[node-csgo](https://github.com/joshuaferrara/node-csgo) is a really powerful plugin for CS:GO, also used by csgostats.gg to get the matches. Note that even csgostats uses the API introduced with the 9/17/2019 CS:GO update.
What we needed to do was not in the cards for node-csgo, but it is still worth mentioning why. 

It is possible to retrieve the link in two ways:
- from the sharecode, using `CSGO.SharecodeDecoder(string code).decode();` This call should return the MatchID, OutcomeID and TokenID needed to reconstruct the link.
Unfortunately, CS:GO sharecodes are intentionally made not to be publically available and cannot be retrieved in any way unless the player shares them with you or allows the third party website to retrieve them through the Steam API.
- directly, using `requestRecentGames()` : Requests a list of recent games for the currently logged in account. By listening for the `matchList` event for the game coordinator's response you will find the download link as: `"map":"http://replay124.valve.net/730/003072985384448163905_0699089210.dem.bz2"` . Although very convenient, as you wouldn't need any sharecode, it cannot be a solution because you would need to make the player log-in instead, which is clearly not feasable.

### Our Choice: hltv.org

So, the only way we could retrieve the matches was through third-party websites. 

[hltv](https://hltv.org) is an extremely popular website used to track Pro CS:GO Competitive Matches. It allows us to track down a specific player and retrieve all his previous matches. 
It is noteworthy that hltv.org downloads the match directly, exactly like any other download, without using any Steam Protocol or API whatsoever, so it is a much easier alternative.

### Web Scraping in Python

In order to download the matches we wrote a Python script that scrapes the hltv website using Selenium Python API. 

Make sure you `pip install selenium` before running the script. 

It basically loads the target player page where all his matches are listed, then it selects a match by scraping the table, opening its "overview" page and clicking the `More info on match page` button to get to the final page. Finally it downloads the match using the dedicated `GOTV Demo` button.

Example: `Player: pashaBiceps`
```
	Match List -> https://www.hltv.org/stats/players/matches/317/pashabiceps
	Match x -> https://www.hltv.org/stats/matches/mapstatsid/90233/heretics-vs-youngsters?contextIds=317&contextTypes=player
	More Info Page -> https://www.hltv.org/matches/2335421/youngsters-vs-heretics-lootbet-season-3
	Download Link -> https://www.hltv.org/download/demo/51659
```

Note: As of right now, the script is almost done. The actual download of the file is a bit tricky, as the script gets stucked in the downloading process and after some time Windows throws an `Unexpected parameter` exception and makes the computer crash. We are trying to figure out why this is happening and how to solve it.

## The Parser: demoinfogo

### Why we chose it

[demoinfogo](https://github.com/ValveSoftware/csgo-demoinfo) is the official CS:GO opensource parser developed by Valve Software written in C/C++. The fact that it comes from Valve itself is a compelling reason to use it, even though it doesn't really come with any documentation on how it works on a deeper level. 

### Building demoinfogo on Windows

Demoinfogo requires Visual Studio to build the solution.

In order to build demoinfogo on Windows, follow these steps:

1. Download [protobuf-2.5.0.zip](https://github.com/google/protobuf/releases/download/v2.5.0/protobuf-2.5.0.zip) and extract it into the `parser` folder. This creates the folder `parser/protobuf-2.5.0`.
2. Download the Protobuf compiler [protoc-2.5.0.zip](https://github.com/google/protobuf/releases/download/v2.5.0/protoc-2.5.0-win32.zip) and extract it into the `parser/protoc-2.5.0-win32` folder.
3. Open `parser/protobuf-2.5.0/vsprojects/protobuf.sln` in Microsoft Visual Studio 2017. Allow Visual Studio to convert the projects.
4. Build the *Release* configuration of `libprotobuf`. Building any other projects is not required.
5. Open `parser/demoinfogo.vcxproj` in Microsoft Visual Studio 2017. Building the Release configuration creates the binary `parser/demoinfogo.exe`

### Reverse Engineering the Parser and Modifying it to suit our needs

First of all, demoinfogo doesn't natively output to a file, it just uses `printf()` functions to print the information to the console. This prevented us to log the data and analyze it. This is why we figured out a very easy way of redirecting the output to a file using the [`freopen`](http://www.cplusplus.com/reference/cstdio/freopen/) C++ function. In demoinfogo.cpp you will find:

		freopen(file.c_str(), "w", stdout);
		DemoFileDump.DoDump();
		fclose(stdout);

Encapsulating the `DemoFileDump.DoDump()` call between freopen and fclose enabled us to log every match in a dedicated .txt file, without changing anything else in the source code.

Of course demoinfogo parses the whole match and logs way too much information, the majority of which is not useful to us. As you can see in demoinfogo.cpp, the application is able to take in some optional arguments. 

Already, `-deathscsv`, `-stringtables`, `-datatables`,  are out the window. Calling the parser with `-gameevents -extrainfo -nofootsteps -nowarmup -packetentities -netmessages` discards a lot of data we don't need and keeps just the bare minimum.

As you can see in the `/test` folder in this repository, we parsed test demos of matches we played in a private server. Every test match consists in single actions, like turning the camera right, moving right, combining the two, and so on. This way we could see which parameters changed and deduce what the values held in them meant. 

We are working on plotting those parameters on a graph to help us in the learning process.

From the `DT_CSPlayer` (Net?) Table we found some useful data about the player. In particular:
- MouseX, MouseY
- PlayerPositionX, PlayerPositionY, PlayerPositionZ
- PlayerVelocityX, PlayerVelocityZ

The following text snippet has been extracted from the dump of a parsed test match, and shows the table fields during a single tick:

```
	Table: DT_CSPlayer
	Field: 0, m_flSimulationTime = 66
	Field: 1, m_nTickBase = 2567
	Field: 2, m_vecOrigin = 279.852173, 2411.995361
	Field: 3, m_vecOrigin[2] = -120.992668
	Field: 4, m_vecVelocity[0] = 102.868484
	Field: 5, m_vecVelocity[1] = -54.856739
	Field: 7, m_vecOrigin = 279.852173, 2411.995361
	Field: 8, m_vecOrigin[2] = -120.992668
	Field: 20, m_angEyeAngles[0] = 0.933838
	Field: 21, m_angEyeAngles[1] =333.088989
```
At first glance, you would think that `m_nTickBase = 2567` holds the current tick, but actually it doesn't. Before dumping the table, a net message is sent.
```
	---- CNETMsg_Tick (12 bytes) -----------------
	tick: 2564
```
As you can see, `m_nTickBase` is 3 ticks ahead of the tick dumped by the `CNETMsg_Tick` message, which is very odd. Being ticks a server-side feature, we decided to trust the CNET Message over the nTickBase from the PlayerTable. - We will make some tests to back up our decision,  though.

Fields 20-21 contain the angle of the player camera, i.e. where he is looking and aiming using the mouse. In detail, the mouse position is represented with a Cartesian plane, where `m_angEyeAngles[0]` is the Y coordinate, whereas `m_angEyeAngles[1]` is the X coordinate. 

Fields 2-3 contain the player's position relative to the origin. Precisely, `m_vecOrigin = 279.852173, 2411.995361` contains both the X and Y coordinates, respectively at indexes 0 and 1, whilst `m_vecOrigin[2] = -120.992668` contains the Z coordinate.

Fields 4-5 contain `m_vecVelocity[0]` and `m_vecVelocity[1]`, which represent the player's velocity relative to his movements in the map. While we wait for other tests, we assume that the two velocities measured are the ones along the X and Z axis, as they would track movements in every direction. Y axis velocity is stored in `m_vecVelocity[2]` (Field 6), and it only changes during jumps and falls, thus it will be logged just when such events occur. 

Actually, every velocity is only logged if it changes, but, compared to Y velocity, X and Z velocities are the ones that change the most. Moreover, they go "hand in hand" in the majority of the times. This is because, statistically speaking, there is a very small chance that the player will move perfectly along one of those axis. 


## Automating the Parsing of the Match Pool

### autoparse.py

As the match pool is very large, parsing every match manually is just not feasable.

So, given the folder where all `.dem` matches are saved, the script will call a shell command for each match, telling demoinfogo to parse it. The `.txt` log file will be saved in `parser/logs` folder.

If any of the subprocesses return an exit code different than `1`, (default exit code of demoinfogo), then that means the parsing was not successful. After finishing the parsing of all the match pool, you will find the failed match name listed in the report.

To setup the script, make sure you edit `demospath` in the source code to match your own demo folder. Then run the script with `python3 autoparse.py`.
