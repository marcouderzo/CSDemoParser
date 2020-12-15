# Project Worklog

This text file is used to keep track of the work being done so far, as well as to give a detailed and exhausive explaination about what we have found out during the project and the reasonings behind our decisions.

Students Involved in the Project:
- [Marco Uderzo](https://github.com/marcouderzo)
- [Samuel Kostadinov](https://github.com/Neskelogth)

## Checklist

**Matches**
- [x] CS:GO Demo Retrievement: Feasibility Study and Decisions

**Scripts**
- [x] Create the Download Script
- [x] Create the AutoParse Script

**Parser Understanding**
- [x] General Understanding of demoinfogo
- [x] Find out Player Tables with Camera, Position, Velocity
- [x] Find out Player Events

**Parser Modifications**
- [x] Filter Player Table Output based on Player EntityID
- [x] Filter Player Events Output based on Player userID
- [ ] Clean Up Output
- [ ] Format Parser Output as Required


## Important note

If your pc has Avast Antivirus, make sure to turn it off. The parser will not work properly if you leave it running.

## Project Requirements

Before you start, make sure the following tools are installed:

- Visual Studio 2017 (or later version) : you will need it in order to compile libprotobuf and the parser itself.
- Google Chrome : used by autodownload.py as our webdriver of choice
- Python 3.8.6 (or later version) : you will need it in order to run the python scripts.
- Selenium (Python Module) : used by the autodownload.py script for scraping the web.
- Pyunpack (Python Module) : used by the autodownload.py script for unpacking the .rar match archives. 

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

It basically loads the target player page where all his matches are listed, then it selects a match by scraping the table, opening its "overview" page and clicking the `More info on match page` button to get to the final page. Finally it downloads the match using the dedicated `GOTV Demo` button.

Example: `Player: pashaBiceps`
```
	↳ https://www.hltv.org/stats/players/matches/317/pashabiceps
	 ↳ https://www.hltv.org/stats/matches/mapstatsid/90233/heretics-vs-youngsters?contextIds=317&contextTypes=player
	  ↳ https://www.hltv.org/matches/2335421/youngsters-vs-heretics-lootbet-season-3
	   ↳ https://www.hltv.org/download/demo/51659
```

You can read the documentation on how it works in detail [here](https://github.com/marcouderzo/CSDemoParser/blob/main/documentation/autodownload%20Script%20Documentation.md)

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

### Understanding the Parser: Tests & Output Analysis

First of all, demoinfogo doesn't natively output to a file, it just uses `printf()` functions to print the information to the console. This prevented us to log the data and analyze it. This is why we figured out a very easy way of redirecting the output to a file using the [`freopen`](http://www.cplusplus.com/reference/cstdio/freopen/) C++ function. In demoinfogo.cpp you will find:
```
freopen(file.c_str(), "w", stdout);
DemoFileDump.DoDump();
fclose(stdout);
```

Encapsulating the `DemoFileDump.DoDump()` call between freopen and fclose enabled us to log every match in a dedicated .txt file, without changing anything else in the source code.

We made sure that the log file had the same name of the demo. All of this was done by figuring out that the parser tries to open the demo with `DemoFileDump.Open( argv[ nFileArgument ] )` (see line 130 of demoinfogo.cpp). Thus, we stored `argv[ nFileArgument ]` into a string variable and erased everything until the last occurence of '/', effectively removing the whole path to the file, and then we removed the file extension. Note that C++ uses backslashes as a line continuation character. The autoparse.py script already replaces them with '/', so you don't have to deal with them. If you decide to call the parser directly from the command line instead, make sure you only use forward slashes in your path.

Of course demoinfogo parses the whole match and logs way too much information, the majority of which is not useful to us. As you can see in demoinfogo.cpp, the application is able to take in some optional arguments. 

**Update: See Parser Modifications** Already, `-deathscsv`, `-stringtables`, `-datatables`,  are not necessary whatsoever. This discards a lot of data we don't need.

The set of arguments of choice is: `-gameevents -extrainfo -nofootsteps -nowarmup -packetentities -netmessages`. We don't need footsteps, as they are events that have more to do with sound and surrounding awareness of a player rather than with the player himself. We also decided to skip match warmups, as they are not so much interesting to log. If they are something you want to include in the log, remove that argument.

As you can see in the `/test` folder in this repository, we parsed test demos of matches we played in a private server. Every test match consists in single actions, like turning the camera right, moving right, combining the two, and so on. This way we could see which parameters changed and deduce what the values held in them meant. 

We are working on plotting those parameters on a graph to help us in the learning process.

**Player Data**

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

**Player Events**

Let's now talk about player events. The main ones are:
- `weapon_fire`
- `weapon_reload`
- `player_jump`
- `weapon_zoom`
- `weapon_zoom_rifle`
- `item_pickup`
- `item_equip`

**Weapon Fire**

A major player event to consider is the `weapon_fire` one.

```
weapon_fire
{
	 userid: Mark (id:2)
	 position: -390.778503, 2017.119141, -127.329865
	 facing: pitch:5.311890, yaw:184.411011
	 team: CT
	 weapon: weapon_m4a1_silencer 
	 silenced: 1 
}
```

`userid` is the unique ID the player is given by the server at the start of the match. `position` is the position of the player at the time of the event. 

`pitch` represents the up/down movement of the mouse, `yaw` represents the right/left one. In CS:GO, if you shoot with an automatic rifle holding down the left mouse button, the gun will naturally recoil with a pattern, which is specific to the gun itself. So, in order to shoot precisely, you need to counteract the recoil pattern with a mirrored mouse movement (i.e. spray control). While testing we figured out that if no mouse movement is present, the pitch and yaw parameters don't change. On the other hand, if spray control is performed, the previously mentioned parameters change, reflecting the mouse movements. As far as we understand, this feature could be used as an additional parameter for player recognition, as everyone has a different accuracy of "drawing" the mirrored recoil pattern.

Note that grenades and similar items are not logged using the `grenade_thrown` event, as we would have thought. Strangely enough, throwing such items is considered a `weapon_fire` event.

**Weapon Reload**

The `weapon_reload` event is triggered when a player reloads his gun. 
```
weapon_reload
{
	  userid: Mark (id:2)
	  position: 182.250000, 2439.010010, -120.968750
	  facing: pitch:359.445190, yaw:356.643677
	  team: CT
}
```
The parameters listed are the same as before.

**Player Jump**

Then, the `player_jump` event.

```
player_jump
{
	  userid: Mark (id:2)
	  position: 351.391998, 2352.939941, -120.504387
	  team: CT
}
```

It is a pretty interesting one, as it can be a parameter to look into when trying to recognize a player. Skilled CS:GO players use a technique called Bunny Hopping to move faster. It is done by jumping repeatedly while changing direction right to left and vice versa, pretty much in a zig-zag. The technique used is pretty much the same, but, exactly like with the spray control, everyone has its own peculiar way of doing it, whether it is timing, synchronization or movement pattern.

**Aiming**

Let's talk about aim related events. In CS:GO, only sniper rifles and a couple of automatic rifles allow zooming in and out (i.e. aiming).

The `weapon_zoom` event is fired each time a player zooms in (or out) their weapon. This only fires on sniper rifles.

```
descriptors {
  eventid: 133
  name: "weapon_zoom"
  keys {
    type: 4
    name: "userid"
  }
```

The `weapon_zoom_rifle` event is fired when a player zooms in with non-sniper rifles.

```
descriptors {
  eventid: 136
  name: "weapon_zoom_rifle"
  keys {
    type: 4
    name: "userid"
  }
```

**Crouching**

As of right now, we haven't found any events regarding crouching in the demo descriptors. What we have found, instead, is that `m_vecViewOffset[2]` is logged just once in all our tests, but it pops up a bunch of times in the crouch test demo. It turned out that `m_vecViewOffset` is the position of the eyes from `vecOrigin`.

```
Field: 14, m_vecViewOffset[2] = 64.062561
Field: 14, m_vecViewOffset[2] = 62.936462
Field: 14, m_vecViewOffset[2] = 59.933529
Field: 14, m_vecViewOffset[2] = 56.054741
Field: 14, m_vecViewOffset[2] = 51.800587
Field: 14, m_vecViewOffset[2] = 48.172043
Field: 14, m_vecViewOffset[2] = 46.044968

Field: 14, m_vecViewOffset[2] = 47.671555
Field: 14, m_vecViewOffset[2] = 51.925709
Field: 14, m_vecViewOffset[2] = 57.055717
Field: 14, m_vecViewOffset[2] = 61.685238
Field: 14, m_vecViewOffset[2] = 63.937439
Field: 14, m_vecViewOffset[2] = 64.062561
Field: 14, m_vecViewOffset[2] = 64.062561
```

As you can see, the first chunck seems to be the descending part of the crouch action, from `64.062561` to `46.044968`. The second one is the ascending part, from `47.671555` back to `64.062561`. So we assume that the `64.062561` value represents the standing state, and `46.044968` represents the crouched state.

**Equipment, Buying Weapons & Items, Picking them Up from the Ground**

Let's talk about `item_equip` and `item_pickup` events. The `item_pickup` event is triggered when a player picks up an item from the ground. The `item_equip` event states the default equipment / equipment at the start of a new round. When a player buys a weapon both `item_equip` and `item_pickup` are triggered in this order. When a player buys an item (e.g. grenade), the `item_pickup` event alone is triggered.

```

item_equip
{
 userid: Mark (id:2)
  position: 2973.000000, 250.000000, 1613.031250
  facing: pitch:0.000000, yaw:182.005005
  team: T
 item: ump45 
 defindex: 24 
 canzoom: 0 
 hassilencer: 0 
 issilenced: 0 
 hastracers: 1 
 weptype: 2 
 ispainted: 0 
}

item_pickup
{
 userid: Mark (id:2)
  position: 2973.000000, 250.000000, 1613.031250
  facing: pitch:0.000000, yaw:182.005005
  team: T
 item: ump45 
 silent: 1 
 defindex: 24 
}

```

**Player Death**

The `player_death` event is triggered when a player dies. 

```

player_death
{
 userid: KRIMZ (id:24)
  position: -1328.922729, 2227.859619, 2.369247
  facing: pitch:352.699585, yaw:333.061523
  team: T
 attacker: mou (id:8)
  position: -1079.365845, 2109.473633, 60.030960
  facing: pitch:11.332397, yaw:152.973633
  team: CT
 assister: 0 
 weapon: usp_silencer 
 weapon_itemid: 7288248617 
 weapon_fauxitemid: 17293822569121710141 
 weapon_originalowner_xuid: 76561198012944495 
 headshot: 1 
 dominated: 0 
 revenge: 0 
 penetrated: 0 
 noreplay: 0 
}

```

The useful data in this event are the `userid`, `position`, `pitch`, `yaw` of the dead player and the attacker, as well as the weapon used to kill and weather or not it was a headshot.


**Bomb Planted, Bomb Defused**

The `bomb_planted` event is triggered when a player plants the bomb.

```
bomb_planted
{
 userid: twist (id:4)
  position: -1360.003052, 2576.968750, 5.403275
  facing: pitch:15.880737, yaw:33.854370
  team: T
 site: 364 
}
```
`Position`, `pitch` and `yaw` are useful in order to know where the player plants the bomb inside the bombsite. 

The `bomb_planted` event is triggered when a player defuses the bomb.

```
bomb_defused
{
 userid: Hobbit (id:7)
  position: 991.971619, 2447.164063, 96.031250
  facing: pitch:39.863892, yaw:92.570801
  team: CT
 site: 367 
}

```

**Round MVP (Most Valuable Player)**

The `round_mvp` event is triggered at the end of every round, announcing the Most Valuable Player of the round (most kills, longest time alive...)

```
round_mvp
{
 userid: Hobbit (id:7)
  position: 991.971619, 2447.164063, 96.031250
  facing: pitch:39.863892, yaw:92.570801
  team: CT
 reason: 3 
 musickitmvps: 0 
}
```
`Position`, `pitch` and `yaw` show where the player is when the event is triggered. `Reason` key is yet to be discovered.

**Finding Event IDs**

In the .proto files, there isn't any event list in the form of `GameEvent1: name="name", event_id=id`. Instead, every demo has a `m_GameEventList`, which is a `CSVCMsg_GameEventList` that inherits from `::google::protobuf::Message`. Dumping the `T msg` that is assigned to `CSVCMsg_GameEventList`, we get a list of all game events, each of them with its own descriptors. A `CSVCMsg_GameEvent` is a class that also inherits from `::google::protobuf::Message`. Inside the `CSVCMsg_GameEvent` class, an useful method can be found: `inline ::google::protobuf::int32 eventid() const`. By calling it when the game event list is dumped, we were able to match the event name and the id and thus make an event list ourselves. 

**More Info**

A Full event list is available [here](http://wiki.sourcepython.com/developing/events/csgo.html)

CS:GO Data PreProcessing [Research Paper](https://www.researchgate.net/publication/318873037_Data_Preprocessing_of_eSport_Game_Records_-_Counter-Strike_Global_Offensive) from Charles University, Prague.











### Modifying the Parser

As the parser outputs using `printf`, we decided to filter the `printf` calls, making them trigger only when we wanted to log something useful.

**Setting The Parser Arguments**

Calling the parser with arguments can be annoying and makes the shell commands unnecessarily verbose, so we decided to set them in the source code and be done with them.


**Cleaning up the output: Useless Printfs**

We commented out `printfs` calls that were unrelated with the player itself, in order to still keep them in case of further reuse of the parser.

**Global Extern Player Variables**

In order to share the SteamID (`xuid`), UserID and EntityID between multiple files and not having issues with the Linker, we created a new `GlobalPlayerInfo.h` file with those variables declared as extern.

Those variables are assigned in `DumpStringTable()` when the parser finds the `PlayerInfo` with the matching `SteamID`.

```
bool DumpStringTable( CBitRead &buf, bool bIsUserInfo )
{
	//other code
	
	if (playerInfo.xuid == targetPlayerSteamID)
	{
		userID = playerInfo.userID;
		entityID = playerInfo.entityID;
		printf("TROVATO TARGET PLAYER %llu , %d, %d \n", targetPlayerSteamID, userID, entityID);
	}
	
	//other code
}
```
**Handling Messages**

The only useful message is the CNETMsgTick. Thus, we made the parser print the message only if its type was a "CNETMsg_Tick". This particular message was originally printed with `vprintf(fmt, vlist)`, and contained other unnecessary information about `host_computationTime`. Having to deal with a function with variable arguments, and being stuck with using a `va_list`, we switched to `vsprintf`, stored the message into a string, and then only kept the tick-related portion of it. We finally convert the string to an integer and store it in currentTick, which is a member variable of the CDemoFileDump class.

```
void CDemoFileDump::MsgPrintf( const ::google::protobuf::Message& msg, int size, const char *fmt, ... )
{
	if ( g_bDumpNetMessages )
	{
		va_list vlist;
		const std::string& TypeName = msg.GetTypeName();

		// Print the message type and size
		if (TypeName == "CNETMsg_Tick")
			printf("---- %s (%d bytes) -----------------\n", TypeName.c_str(), size);

		va_start(vlist, fmt);
		if (TypeName == "CNETMsg_Tick")
		{
			char res[500];
			vsprintf(res, fmt, vlist);
			std::string s = res;
			auto endOfTickDelimiter = s.find_first_of('h');
			s.erase(endOfTickDelimiter);
			s.erase(0, s.find_last_of(':')+1);
			currentTick = std::stoi(s);
			printf("------ Tick = %ld ------\n", currentTick);
			
		}
		va_end(vlist);
	}
}
```

**Handling Tables: Only Keeping Track of the Target Player's DT_CSPlayer Table**

The `ReadNewEntity( CBitRead &entityBitBuffer, EntityEntry *pEntity )` function reads the Table Name and then for each field of the table itself, it will call `DecodeProp()` to print it. 
First of all, we modified `ReadNewEntity()` to only print the table name if it is related to the target player.

```
bool ReadNewEntity( CBitRead &entityBitBuffer, EntityEntry *pEntity )
{
	//other code
	
	if (pTable->net_table_name() == "DT_CSPlayer" && pEntity->m_nEntity == entityID)
	{
		printf("[beforePrintNetTables]");
		printf("Table: %s\n", pTable->net_table_name().c_str());
	}
	
	//other code
}
```
Then, it was time to modify `DecodeProp().`

```
Prop_t *DecodeProp( CBitRead &entityBitBuffer, FlattenedPropEntry *pFlattenedProp, uint32 uClass, int nFieldIndex, bool bQuiet )
{
	//other code

	if (pSendProp->var_name() == "m_vecVelocity[0]" ||
	    pSendProp->var_name() == "m_vecVelocity[1]" ||
	    pSendProp->var_name() == "m_vecVelocity[2]" ||
	    pSendProp->var_name() == "m_vecOrigin" ||
	    pSendProp->var_name() == "m_vecOrigin[2]" ||
	    pSendProp->var_name() == "m_angEyeAngles[0]" ||
	    pSendProp->var_name() == "m_angEyeAngles[1]")
	{
		printf("Field: %d, %s = ", nFieldIndex, pSendProp->var_name().c_str());
		hasToPrint = true;
	}

	// other code

	if (!bQuiet && hasToPrint)
	{
		pResult->Print();
	}
	
	//other code
}	

```

After modifiying it, we realized it printed the right fields, but of every player in the match. In order to fix it, we would have to pass an additional argument to `DecodeProp()`, potentially breaking the code somewhere else. Thus, we decided to play it safe and created a new function `Prop_t *DecodePropWithEntity()`, which is basically the same as the original one, but it also takes in an `EntityEntry`, used to check whether or not the Entity is actually the target player or someone else. 

```
Prop_t *DecodePropWithEntity(CBitRead &entityBitBuffer, FlattenedPropEntry *pFlattenedProp, uint32 uClass, int nFieldIndex, bool bQuiet, void *pEntity)
{
	EntityEntry* Entity = static_cast<EntityEntry*>(pEntity);
	const CSVCMsg_SendTable::sendprop_t *pSendProp = pFlattenedProp->m_prop;
	
	//other code
	
	if ((pSendProp->var_name() == "m_vecVelocity[0]" ||
	pSendProp->var_name() == "m_vecVelocity[1]" ||
	pSendProp->var_name() == "m_vecVelocity[2]" ||
	pSendProp->var_name() == "m_vecOrigin" ||
	pSendProp->var_name() == "m_vecOrigin[2]" ||
	pSendProp->var_name() == "m_angEyeAngles[0]" ||
	pSendProp->var_name() == "m_angEyeAngles[1]") && Entity->m_nEntity==entityID)
	{
		if (nFieldIndex != 6 && nFieldIndex != 16)
		{
			printf("Field: %d, %s = ", nFieldIndex, pSendProp->var_name().c_str());
			hasToPrint = true;
		}
	}
	
	// other code
}
```

**Parsing the chosen Game Events of the Target Player**

In `ParseGameEvent()`,  the `CSVCMsg_GameEvent msg` has its own `eventid()` method, which obviously returns the `eventID`. We check if the `eventID` is actually the one we want, else we return. Then we search in the `msg` keys the userID of the player, and if it is actually an event from the target player, we let the parser print it, else we return.

```
void ParseGameEvent( const CSVCMsg_GameEvent &msg, const CSVCMsg_GameEventList::descriptor_t *pDescriptor )
{
	//other code

	if (msg.eventid() != 169 && //jump
		msg.eventid() != 129 && //weapon_fire
		msg.eventid() != 132 && //weapon_reload
		//msg.eventid() != ? && //grenade_thrown (not found)
		msg.eventid() != 167 && //bullet_impact
		msg.eventid() != 134 && //silencer_detach
		msg.eventid() != 133 && //weapon_zoom
		msg.eventid() != 136 && //weapon_zoom_rifle
		msg.eventid() != 138 && //item_pickup 
		msg.eventid() != 139 && //ammo_pickup
		msg.eventid() != 140 && //item_equip
		msg.eventid() != 106 && //bomb_abortplant
		msg.eventid() != 156 && //flashbang_detonate
		msg.eventid() != 155 && //hegrenade_detonate
		msg.eventid() != 157 && //smokegrenade_detonate
		msg.eventid() != 107 && //bomb_planted
		msg.eventid() != 104 && //item_purchase
		msg.eventid() != 172) {	//door_moving
		return;
	}

	int NumKeys = msg.keys().size();
	for (int i = 0; i < NumKeys; i++)
	{
		const CSVCMsg_GameEventList::key_t& Key = pDescriptor->keys(i);
		const CSVCMsg_GameEvent::key_t& KeyValue = msg.keys(i);
		if (Key.name().compare("userid") == 0 || Key.name().compare("attacker") == 0 || Key.name().compare("assister") == 0)
		{
			player_info_t *pPlayerInfo = FindPlayerInfo(KeyValue.val_short());
			if (KeyValue.val_short() != userID)
				return;
			printf("Event from TargetPlayer with userid: %d \n", KeyValue.val_short());
		}
	}	
	
	//other code
}
```




## Automating the Parsing of the Match Pool

### autoparse.py

As the match pool is very large, parsing every match manually is just not feasable. So, we decided to write a simple script to automate the parsing process.

You can read the documentation on how it works in detail [here](https://github.com/marcouderzo/CSDemoParser/blob/main/documentation/autoparse%20Script%20Documentation.md)
