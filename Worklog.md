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
- [x] Create the Dataset Validation Script

**Parser Understanding**
- [x] General Understanding of demoinfogo
- [x] Find out a Complete Event List
- [x] Create *Ad-hoc* Demos for Testing
- [x] Find out Player Tables with Camera, Position, Velocity
- [x] Find out Player Events

**Parser Modifications**
- [x] Filter Player Table Output based on Player EntityID
- [x] Filter Player Events Output based on Player userID
- [x] Clean Up Output
- [x] Format Parser Output as Required


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

**Finding an Event List with IDs**

In the .proto files, there isn't any event list in the form of `GameEvent1: name="name", event_id=id`. Instead, every demo has a `m_GameEventList`, which is a `CSVCMsg_GameEventList` that inherits from `::google::protobuf::Message`. Dumping the `T msg` that is assigned to `CSVCMsg_GameEventList`, we get a list of all game events, each of them with its own descriptors. A `CSVCMsg_GameEvent` is a class that also inherits from `::google::protobuf::Message`. Inside the `CSVCMsg_GameEvent` class, an useful method can be found: `inline ::google::protobuf::int32 eventid() const`. By calling it when the game event list is dumped, we were able to match the event name and the id and thus make an event list ourselves. 

**Player Events**

Let's now talk about player events. As you will see, pitch, yaw and position are not inherently part of the events: there are no such keys. From now, whatever piece of information that is not mentioned in the event's key table is taken directly from the player entity (see the DT_CSPlayer Table mentioned before).

The player events we agreed to keep are the following:

- `weapon_fire`
- `weapon_reload`
- `player_jump`
- `player_crouch` (Custom Event)
- `player_death`
- `weapon_zoom`
- `weapon_zoom_rifle`
- `item_pickup`
- `item_equip`
- `item_purchase`
- `ammo_pickup`
- `bullet_impact` *
- `silencer_detach` *
- `bomb_planted`
- `bomb_defused`
- `bomb_beginplant`
- `bomb_abortplant`
- `bomb_begindefuse`
- `bomb_abortdefuse`
- `bomb_dropped`
- `defuser_dropped`
- `bomb_pickup`
- `defuser_pickup`
- `round_mvp`
- `grenade_thrown` *
- `flashbang_detonate`
- `hegrendade_detonate`
- `smokegrenade_detonate`
- `tagrenade_detonate`
- `decoy_detonate`
- `molotov_detonate
- `player_falldamage`
- `player_blind`
- `door_moving`

**Weapon Fire**

A major player event to consider is the `weapon_fire` one.
This event is fired each time a bullet is fired, or a projectile thrown, by a player.

| Name      | Description                                       | Type
|-----------|-------------------------------------------------  | -----
| silenced  |  True if the weapon has a silencer active.        |bool
| userid    |	The userid of the player that fired the weapon.	|short
| weapon    |	The type of weapon that was fired.	        |string

Output example:

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

The `weapon_reload` event is fired when a player reloads their weapon by pressing their ‘reload’ button. Automatic reloading does not fire this event.

| Name      | Description                                       | Type
|-----------|-------------------------------------------------  | -----
| userid    |	The userid of the player that reloaded their weapon.	|short


Output Example:

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

| Name      | Description                                       | Type
|-----------|-------------------------------------------------  | -----
| userid    |	The userid of the player that jumped.	|short

Output Example:

```
player_jump
{
	  userid: Mark (id:2)
	  position: 351.391998, 2352.939941, -120.504387
	  team: CT
}
```

It is a pretty interesting one, as it can be a parameter to look into when trying to recognize a player. Skilled CS:GO players use a technique called Bunny Hopping to move faster. It is done by jumping repeatedly while changing direction right to left and vice versa, pretty much in a zig-zag. The technique used is pretty much the same, but, exactly like with the spray control, everyone has its own peculiar way of doing it, whether it is timing, synchronization or movement pattern.

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

We came up with a solution to simulate this game event in a seamless way. Check the "Modifying the Parser" section for more information.


**Player Death**

The `player_death` event is triggered when a player dies. It the *Modifying the Parser* section we will explain how we can differenciate this event and use it to log both the target player's death and a kill/assist by them.

| Name      | Description                                       | Type
|-----------|-------------------------------------------------  | -----
| assister |	The userid of the player that assisted in the kill (if any). |	short
| attacker |	The userid of the killer. |	short
| dominated |	True (1) if the kill caused the killer to be dominating the victim. |	short
| headshot |	True if the killshot was to the victim’s head hitbox. |	bool
| noreplay |	 N/A	| bool
| penetrated |	The number of objects that were penetrated by the bullet before it struck the victim. |	short
| revenge |	True (1) if the victim was dominating the killer. |	short
| userid |	The userid of the victim. |	short
| weapon |	The type of weapon used to kill the victim. |	string
| weapon_fauxitemid |	Faux item id of weapon killer used. |	string
| weapon_itemid	| Inventory item id of weapon killer used. | string
| weapon_originalowner_xuid |	 	string

Output Example:

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


**Aiming: Weapon Zoom**

Let's talk about aim related events. In CS:GO, only sniper rifles and a couple of automatic rifles allow zooming in and out (i.e. aiming).

The `weapon_zoom` event is fired each time a player zooms in (or out) their weapon. This only fires on sniper rifles.

| Name      | Description                                       | Type
|-----------|-------------------------------------------------  | -----
| userid    |	The userid of the player that zoomed their weapon	|short

Descriptors:

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


| Name      | Description                                       | Type
|-----------|-------------------------------------------------  | -----
| userid    |	The userid of the player that zoomed their weapon	|short

Descriptors:

```
descriptors {
  eventid: 136
  name: "weapon_zoom_rifle"
  keys {
    type: 4
    name: "userid"
  }
```

**Equipment, Buying Weapons & Items, Picking them Up from the Ground**

Let's talk about `item_equip` and `item_pickup` events. The `item_pickup` event is triggered when a player picks up an item from the ground. The `item_equip` event states the default equipment / equipment at the start of a new round. When a player buys a weapon both `item_equip` and `item_pickup` are triggered in this order. When a player buys an item (e.g. grenade), the `item_pickup` event alone is triggered.

**Item Equip**


| Name      | Description                                       | Type
|-----------|-------------------------------------------------  | -----
| canzoom |	True if the weapon has a zoom feature. |	bool
| hassilencer |	True if the weapon has a silencer available. |	bool
| hastracers |	True if the weapon has tracer bullets that show when fired. |	bool
| ispainted |	True if the weapon is painted.	| bool
| issilenced |	True if the weapon has a silencer and it is on.	| bool
| item	| The type of item/weapon that the player equipped. |	string
| userid |	The userid of the player that equipped the item. | short
| weptype |	The weapon type of the item equipped (more below). | short

Output Example:

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
```

**Item Pickup**

| Name      | Description                                       | Type
|-----------|-------------------------------------------------  | -----
| item |  The index of the item the player picked up.        | string
| userid    |	The userid of the player that fired the weapon.	|short
| silent    |	True if the item is a weapon that has a silencer. | bool

Output Example:

```
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
**Item Purchase**

The `item_purchase` event is fired each time a player purchases an item. Actually, we never seen it came up during our events testing sessions, nor in the much longer competitive matches.

| Name      | Description                                       | Type
|-----------|-------------------------------------------------  | -----
|team |	The team number of the player that purchased an item. |	short
|userid	| The userid of the player that purchased an item. |	short
|weapon	| The type of item that the player purchased. |	string

We have no output example available.

**Ammo Pickup**

The `ammo_pickup` event is triggered when a player picks up weapon ammos. We never found a single istance of this event being logged. 

| Name      | Description                                       | Type
|-----------|-------------------------------------------------  | -----
| index	 |	| long
| item	 |	| string
| userid |	 |	short

No Output Example available.

**Silencer Detach**

The `silencer_detach` event is triggered when a player detaches the silencer from their weapon.

| Name      | Description                                       | Type
|-----------|-------------------------------------------------  | -----
|userid	| |	short

No Output Example available. 

**Bomb Planted, Bomb Defused**

The `bomb_planted` event is triggered when a player plants the bomb.

| Name      | Description                                       | Type
|-----------|-------------------------------------------------  | -----
| site	| The index of the site where the bomb was planted. |	short
| userid |	The userid of the player that planted the bomb.	| short

Output Example:

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



The `bomb_defused` event is triggered when a player defuses the bomb.


| Name      | Description                                       | Type
|-----------|-------------------------------------------------  | -----
| site	| The index of the site where the bomb was defused. |	short
| userid |	The userid of the player that defused the bomb.	| short

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

The `bomb_abortplant` is triggered when a player aborts the bomb plant.

| Name      | Description                                       | Type
|-----------|-------------------------------------------------  | -----
| userid |	The userid of the player that aborted the bomb plant.	| short


The `bomb_abortdefuse` is triggered when a player aborts the bomb defuse.

| Name      | Description                                       | Type
|-----------|-------------------------------------------------  | -----
| userid |	The userid of the player that aborted the bomb defuse.	| short


The `bomb_beginplant` is triggered when a player begins the bomb plant.

| Name      | Description                                       | Type
|-----------|-------------------------------------------------  | -----
| userid |	The userid of the player that began planting the bomb.	| short

**Output Example**

```
bomb_beginplant
{
 userid: SWOLEfREAKAZOiD (id:40)
  position: -1166.488647, -79.961365, 98.031250
  facing: pitch:4.619751, yaw:96.531372
  team: T
 site: 504 
}
```

The `bomb_begindefuse` is triggered when a player begins the bomb defuse.

| Name      | Description                                       | Type
|-----------|-------------------------------------------------  | -----
| userid |	The userid of the player that began defusing the bomb.	| short
| haskit |	if the player has a defuse kit	| short

**Output Example**

```
bomb_begindefuse
{
 userid: BNBptr (id:35)
  position: -1159.983765, -28.044533, 117.279297
  facing: pitch:55.442505, yaw:279.761353
  team: CT
 haskit: 0 
}
```


**Round MVP (Most Valuable Player)**

The `round_mvp` event is triggered at the end of every round, announcing the Most Valuable Player of the round (most kills, longest time alive...)

| Name      | Description                                       | Type
|-----------|-------------------------------------------------  | -----
| reason |	The reason why the player is the MVP of the round. |	short
| userid |	The userid of the player that was the MVP of the round.	| short

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

**Flashbang Detonation**

This event is fired when a flashbang detonates.

| Name      | Description                                       | Type
|-----------|-------------------------------------------------  | -----
| entityid	| The index of the flashbang that detonated.	| short
| userid	| The userid of the player that threw the flashbang.	| short
| x	| The x coordinate on the map where the flashbang detonated. |	float
| y	| The y coordinate on the map where the flashbang detonated. |	float
| z	| The z coordinate on the map where the flashbang detonated. |	float

Output Example:

```
flashbang_detonate
{
 userid: paszaBiceps (id:48)
  position: 2290.599121, 2342.761475, 128.031250
  facing: pitch:1.494141, yaw:119.674072
  team: CT
 entityid: 592 
 x: 2333.904297 
 y: 2196.434082 
 z: 130.007111 
}
```


**High Explosive Grenade Detonation**

The `hegrenade_detonate` event is fired when a high explosive grenade detonates.

| Name      | Description                                       | Type
|-----------|-------------------------------------------------  | -----
| entityid	| The index of the grenade that detonated.	| short
| userid	| The userid of the player that threw the grenade.	| short
| x	| The x coordinate on the map where the grenade detonated. |	float
| y	| The y coordinate on the map where the grenade detonated. |	float
| z	| The z coordinate on the map where the grenade detonated. |	float

Output Example:

```
hegrenade_detonate
{
 userid: paszaBiceps (id:48)
  position: 709.969910, 2194.751953, 200.633133
  facing: pitch:359.956055, yaw:232.849731
  team: CT
 entityid: 194 
 x: -74.130783 
 y: 1431.750366 
 z: 175.692062 
}
```

**Smoke Grenade Detonation**

The `smokegrenade_detonate` event is fired when a smoke grenade detonates.

| Name      | Description                                       | Type
|-----------|-------------------------------------------------  | -----
| entityid	| The index of the smoke grenade that detonated.	| short
| userid	| The userid of the player that threw the smoke grenade.	| short
| x	| The x coordinate on the map where the smoke grenade detonated. |	float
| y	| The y coordinate on the map where the smoke grenade detonated. |	float
| z	| The z coordinate on the map where the smoke grenade detonated. |	float

Output Example:

```
smokegrenade_detonate
{
 userid: paszaBiceps (id:48)
  position: 655.060791, 2631.935547, 213.209351
  facing: pitch:6.207275, yaw:220.770264
  team: CT
 entityid: 199 
 x: 829.143066 
 y: 2247.610596 
 z: 138.758911 
}
```

**Tactic Grenade Detonation**

The `tagrenade_detonate` event is fired when a tactic grenade detonates.

| Name      | Description                                       | Type
|-----------|-------------------------------------------------  | -----
| entityid	| The index of the tactic grenade that detonated.	| short
| userid	| The userid of the player that threw the tactic grenade.	| short
| x	| The x coordinate on the map where the tactic grenade detonated. |	float
| y	| The y coordinate on the map where the tactic grenade detonated. |	float
| z	| The z coordinate on the map where the tactic grenade detonated. |	float

No Output example available.

**Molotov Detonation**

The `molotov_detonate` event is fired when a molotov detonates.

| Name      | Description                                       | Type
|-----------|-------------------------------------------------  | -----
| entityid	| The index of the molotov that detonated.	| short
| userid	| The userid of the player that threw the molotov.	| short
| x	| The x coordinate on the map where the molotov detonated. |	float
| y	| The y coordinate on the map where the molotov detonated. |	float
| z	| The z coordinate on the map where the molotov detonated. |	float

No Output example available.

**Decoy Detonation**

The `decoy_detonate` event is fired when a decoy detonates.

| Name      | Description                                       | Type
|-----------|-------------------------------------------------  | -----
| entityid	| The index of the decoy that detonated.	| short
| userid	| The userid of the player that threw the decoy.	| short
| x	| The x coordinate on the map where the decoy decoy. |	float
| y	| The y coordinate on the map where the molotov decoy. |	float
| z	| The z coordinate on the map where the molotov decoy. |	float

**Output Example**

```
decoy_detonate
{
 userid: SWOLEfood (id:31)
  position: -621.247681, -1829.594849, 145.029633
  facing: pitch:7.443237, yaw:85.984497
  team: T
 entityid: 473 
 x: -1195.489136 
 y: -3041.499268 
 z: 249.889053 
}
```

**Bomb Dropped, Defuser Dropped**

The `bomb_dropped` event is fired when a player drops the bomb.

| Name      | Description                                       | Type
|-----------|-------------------------------------------------  | -----
| entindex |	The index of the c4 entity that was dropped. | 	long
| userid |	The userid of the player that dropped the bomb. |	short

The `defuser_dropped` event is fired when a player drops the bomb.

| Name      | Description                                       | Type
|-----------|-------------------------------------------------  | -----
| entityid	| |	long

**Bomb Pickup, Defuser Pickup**

The `bomb_pickup` event is fired when a player picks up the bomb.

| Name      | Description                                       | Type
|-----------|-------------------------------------------------  | -----
userid |	The userid of the player that picked up the bomb. |	short

**Output Example**

```
bomb_pickup
{
 userid: SWOLEfREAKAZOiD (id:40)
  position: -2398.636719, -1318.219116, 486.440796
  facing: pitch:1.071167, yaw:76.734009
  team: T
}
```

The `defuser_pickup` event is fired when a player picks up a defuser.

| Name      | Description                                       | Type
|-----------|-------------------------------------------------  | -----
userid	The userid of the player that picked up the defuser.	short
entityid |	 	| long

No Output Example available.

**Player Fall Damage**

The `player_falldamage` event is fired when a player sustains damage from falling from a height.

| Name      | Description                                       | Type
|-----------|-------------------------------------------------  | -----
| damage |	The amount of damage the player sustained. |	float
| userid |	The userid of the player that fell. |	short

**Output Example**

```
player_falldamage
{
 userid: SWOLEfREAKAZOiD (id:40)
  position: -1827.862305, 1032.602417, 247.951172
  facing: pitch:26.696777, yaw:266.539307
  team: T
 damage: 6.994048 
}
```

**Player Blid**

The `player_blind` event is fired when a player is blinded by a flashbang.


| Name      | Description                                       | Type
|-----------|-------------------------------------------------  | -----
| userid	| id of the player |	short
| attacker	| player who threw the flashbang |	short
| entityid	| entity id of the flashbang  |	short
| blind_duration	| how much the player was blinded for |	float




**Door Moving**

The `door_moving` event is fired when a door is opened or closed. This event is never triggered, even when we analyzed a dedicated demo in which the player opens and closes a door many times.

| Name      | Description                                       | Type
|-----------|-------------------------------------------------  | -----
| entindex |	The index of the door.	| long
| userid |	The userid of the player that activated the door’s movement. |	short

No Output Example available.

**Bullet Impact**

The `bullet_impact` event is fired when a player shoots their weapon and the bullet impacts a surface. Never got logged during our tests.

| Name      | Description                                       | Type
|-----------|-------------------------------------------------  | -----
| userid |	The userid of the player that fired the bullet.	| short
| x |	The x coordinate on the map where the impact took place. |	float
| y |	The y coordinate on the map where the impact took place. |	float
| z |	The z coordinate on the map where the impact took place. |	float

No Output Example available.


**More Info**

A Full event list is available [here](http://wiki.sourcepython.com/developing/events/csgo.html)


### Modifying the Parser

As the parser outputs using `printf`, we decided to filter the `printf` calls, making them trigger only when we wanted to log something useful.

Most of the code not needed (e.g. useless printf() calls) is commented out. We decided to keep it commented over deleting it for clarity and reuse purposes. 

**Setting The Parser Arguments**

Calling the parser with arguments can be annoying and makes the shell commands unnecessarily verbose, so we decided to set them in the source code and be done with them.


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
	}
	
	//other code
}
```
**Handling Messages**

The only useful message is the CNETMsgTick. Thus, we made the parser print the message only if its type was a "CNETMsg_Tick". This particular message was originally printed with `vprintf(fmt, vlist)`, and contained other unnecessary information about `host_computationTime`. Having to deal with a function with variable arguments, and being stuck with using a `va_list`, we switched to `vsprintf`, stored the message into a string, and then only kept the tick-related portion of it. We finally convert the string to an integer and store it in currentTick, which is an extern variable in `GlobalPlayerInfo.h`

```
void CDemoFileDump::MsgPrintf( const ::google::protobuf::Message& msg, int size, const char *fmt, ... )
{
	if (g_bDumpNetMessages)
	{
		va_list vlist;
		const std::string& TypeName = msg.GetTypeName();


		if (TypeName == "CNETMsg_Tick")
		{
			va_start(vlist, fmt);
			char res[500];
			vsprintf(res, fmt, vlist);
			std::string s = res;
			auto endOfTickDelimiter = s.find_first_of('h');
			s.erase(endOfTickDelimiter);
			s.erase(0, s.find_last_of(':') + 1);
			currentTick = std::stoi(s);
			va_end(vlist);
		}
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

After modifiying it, we realized it printed the right fields, but of every player in the match. In order to fix it, we would have to pass an additional argument to `DecodeProp()`, potentially breaking the code somewhere else. Thus, we decided to play it safe and created a new function `Prop_t *DecodePropWithEntity()`, which is basically the same as the original one, but it also takes in an `EntityEntry`, used to check whether or not the Entity is actually the target player or someone else. (Note that the original DecodeProp() is now as it was.)

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

**Parsing Target Player's Game Events and Formatting the *Action* Output as Required**

In order to format the game events output as required:

```
Action Tick Type playerPositionX playerPositionY playerPositionZ (....and other data depending on the particular event)
```

we came up with different strategies. First of all we pin pointed how the parser deals with game events and where it does it.

In `ParseGameEvent()`,  the `CSVCMsg_GameEvent msg` has its own `eventid()` method, which obviously returns the `eventID`. It seemed like checking the IDs would just work fine to discard the unwanted events, as we already had a complete event list. Later we would have used the `CSVCMsg_GameEventList::descriptor_t *pDescriptor` to check the userid of the player.

```
void ParseGameEvent( const CSVCMsg_GameEvent &msg, const CSVCMsg_GameEventList::descriptor_t *pDescriptor )
{
	// other code
	
	if (msg.eventid() != 169 && //jump
		msg.eventid() != 129 && //weapon_fire
		msg.eventid() != 132 && //weapon_reload
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
		msg.eventid() != 23  && //player_death
		msg.eventid() != 172) //door_moving
	{	
		return;
		
	// other code
}
	
```

While testing, we noticed that some chosen events never got logged, and some discarded ones did instead. We compared the event list with various demos, and we figured out that event IDs were not the same at all! Some of them were offset by two indexes, others were also missing. 

We used a diff checker to look into this. An example of those inconsistencies can be clearly seen in [this diff](https://www.diffchecker.com/zC7OIIba).

Therefore, for consistency purposes, we decided to use the event's `pDescriptor` and check for the event name instead. Indeed, we don't really need the `CSVCMsg_GameEvent &msg` message anyways, if not to check the id of the events.

Let's look at the function in detail:

We start checking if it's a `player_death` event, as it is handled differently. If that's the case, we prepare to handle it later. 

Then we basically check the descriptor's name for the events we are interested in. If that's not an event we care about, we return. As you can see, the logic behind it is the same as before, but without the danger of IDs inconsistency.

Note that the grenade_thrown event is never triggered, not in our parser, nor in the original one. Strangely enough, it is present in the descriptors, but it is missing from this [list](http://wiki.sourcepython.com/developing/events/csgo.html) we used for double-checking.

```
void ParseGameEvent( const CSVCMsg_GameEvent &msg, const CSVCMsg_GameEventList::descriptor_t *pDescriptor )
{
	bool isPlayerDeath = false;
	if (pDescriptor->name().compare("player_death") == 0)
	{
		isPlayerDeath = true;
		//HandlePlayerDeath(msg, pDescriptor);
	}

    	if (	pDescriptor->name() != "player_jump" && //player_jump
		pDescriptor->name() != "weapon_fire" && //weapon_fire
		pDescriptor->name() != "weapon_reload" && //weapon_reload
		pDescriptor->name() != "grenade_thrown" && //grenade_thrown	// NOT FOUND, EVEN THOUGH IT IS PRESENT IN DESCRIPTORS. 
		pDescriptor->name() != "bullet_impact" && //bullet_impact	// Never shows up even when parsing with the original parser
		pDescriptor->name() != "silencer_detach" && //silencer_detach
		pDescriptor->name() != "weapon_zoom" && //weapon_zoom
		pDescriptor->name() != "weapon_zoom_rifle" && //weapon_zoom_rifle
		pDescriptor->name() != "item_pickup" && //item_pickup
		pDescriptor->name() != "ammo_pickup" && //ammo_pickup 
		pDescriptor->name() != "silencer_detach" &&
		pDescriptor->name() != "item_equip" && //item_equip
		pDescriptor->name() != "bomb_beginplant" && //bomb_beginplant
		pDescriptor->name() != "bomb_abortplant" && //bomb_abortplant
		pDescriptor->name() != "bomb_begindefuse" && //bomb_begindefuse
		pDescriptor->name() != "bomb_abortdefuse" && //bomb_abortdefuse
		pDescriptor->name() != "flashbang_detonate" && //flashbang_detonate
		pDescriptor->name() != "hegrenade_detonate" && //hegrenade_detonate
		pDescriptor->name() != "smokegrenade_detonate" && //smokegrenade_detonate
		pDescriptor->name() != "molotov_detonate" && //molotov_detonate
		pDescriptor->name() != "decoy_detonate" && //decoy_detonate
		pDescriptor->name() != "tagrenade_detonate" &&
		pDescriptor->name() != "bomb_planted" && //bomb_planted
		pDescriptor->name() != "bomb_defused" && //bomb_defused
		pDescriptor->name() != "round_mvp" && //round_mvp
		pDescriptor->name() != "item_purchase" && //item_purchase
		pDescriptor->name() != "player_death" && //player_death
		pDescriptor->name() != "bomb_dropped" &&
		pDescriptor->name() != "defuser_dropped" &&
		pDescriptor->name() != "bomb_pickup" &&
		pDescriptor->name() != "defuser_pickup" &&
		pDescriptor->name() != "player_falldamage" &&
		pDescriptor->name() != "player_blind" &&
		pDescriptor->name() != "door_moving") //door_moving 
		{	
			return;
		}
		
		// function continues...

```
Then, we iterate through the event keys, and we check for events that are not `player_death` and that are not about the target player. In this case, we return as we have no interest in logging them.

```
	// ...here
	
	int NumKeys = msg.keys().size();

	for (int i = 0; i < NumKeys; i++)
	{
		const CSVCMsg_GameEventList::key_t& Key = pDescriptor->keys(i);
		const CSVCMsg_GameEvent::key_t& KeyValue = msg.keys(i);
		if (!isPlayerDeath && Key.name().compare("userid") == 0 && KeyValue.val_short() != userID)
			return;
	}
	
	// function continues...
```
We iterate again, but this time we we check for `player_death` events in which our target player is involved, whether it killed someone, assisted a kill or died. In all of those cases, we are interested in the event, so we determine the type of event. This is done by looking at the userid (the victim), at the attacker and at the assister. We set a string with the event type to add to the event name. 

- *player_death_k* : target player killed.
- *player_death_a* : target player assisted a kill.
- *player_death_d* : target player died.


```
	// ...here
	
	bool isEventInteresting = false;

	std::string deathEventType ="";

	for (int i = 0; i < NumKeys; i++)
	{
		const CSVCMsg_GameEventList::key_t& Key = pDescriptor->keys(i);
		const CSVCMsg_GameEvent::key_t& KeyValue = msg.keys(i);
		if (Key.name().compare("userid") == 0 || Key.name().compare("attacker") == 0 || Key.name().compare("assister") == 0)
		{
			player_info_t *pPlayerInfo = FindPlayerInfo(KeyValue.val_short());
			if (isPlayerDeath)
			{
				if ((Key.name().compare("userid") == 0 && KeyValue.val_short() == userID) ||
					(Key.name().compare("attacker") == 0 && KeyValue.val_short() == userID) ||
					(Key.name().compare("assister") == 0 && KeyValue.val_short() == userID))
				{
					isEventInteresting = true;
				}

				if (Key.name().compare("userid") == 0 && KeyValue.val_short() == userID)
					deathEventType = "_d";

				if (Key.name().compare("attacker") == 0 && KeyValue.val_short() == userID)
					deathEventType = "_k";

				if (Key.name().compare("assister") == 0 && KeyValue.val_short() == userID)
					deathEventType = "_a";
			}
		}
	}
	
	// function continues...

```
If the event is a `player_death` event and is not relevant, we just return. Else, we add to the event name the `deathEventType`.

```
	// ...here
	if (!isEventInteresting && isPlayerDeath) return;
	printf("Action %d ", currentTick);

	if ( g_bDumpGameEvents )
	{
		printf( "%s%s ", pDescriptor->name().c_str(), deathEventType.c_str()); // Event Name
	}

	int numKeys = msg.keys().size();
	for ( int i = 0; i < numKeys; i++ )
	{
		const CSVCMsg_GameEventList::key_t& Key = pDescriptor->keys( i );
		const CSVCMsg_GameEvent::key_t& KeyValue = msg.keys( i );

		if ( g_bDumpGameEvents )
		{
			bool bHandled = false;
			if ( Key.name().compare( "userid" ) == 0 || Key.name().compare( "attacker" ) == 0 || Key.name().compare( "assister" ) == 0 )
			{
				bHandled = ShowPlayerInfo( Key.name().c_str(), KeyValue.val_short(), g_bShowExtraPlayerInfoInGameEvents );
			}
			
			//other code
}		

```

The `ShowPlayerInfo()` function is called. We only let the parser print the player position.

```
bool ShowPlayerInfo( const char *pField, int nIndex, bool bShowDetails = true, bool bCSV = false )
{
	// other code
	
	int nEntityIndex = pPlayerInfo->entityID + 1;
	EntityEntry *pEntity = FindEntity( nEntityIndex );
	if ( pEntity )
	{
		PropEntry *pXYProp = pEntity->FindProp( "m_vecOrigin" );
		PropEntry *pZProp = pEntity->FindProp( "m_vecOrigin[2]" );
		if ( pXYProp && pZProp )
		{
			if ( bCSV )
			{
				printf( "%f %f %f ", pXYProp->m_pPropValue->m_value.m_vector.x, pXYProp->m_pPropValue->m_value.m_vector.y, pZProp->m_pPropValue->m_value.m_float );
			}
			else
			{
				printf( "%f %f %f ", pXYProp->m_pPropValue->m_value.m_vector.x, pXYProp->m_pPropValue->m_value.m_vector.y, pZProp->m_pPropValue->m_value.m_float );
			}
		}

		// other code
}	

```
When the function returns to `ParseGameEvent()`, we print additional information, depending on the event.

**OLD: Creating a Custom Crouch Event**

*(This is deprecated, we are handling it in a different way)* - As there is no `crouch_event` in the event list, we came up with a way of simulating such game event (see what we discovered in the parser in the "Understanding the Parser" section).

In `GlobalPlayerInfo.h`, we defined a new extern variable: bool `isPlayerCrouched`.

In the `DecodePropWithEntity()` function, we check for the `m_vecViewOffset[2]` prop and the correct `entityID`. If we find both of them, we can be sure that's about the target player offsetting from `vecOrigin`, which only happens when a player crouches.

```
Prop_t *DecodePropWithEntity(CBitRead &entityBitBuffer, FlattenedPropEntry *pFlattenedProp, uint32 uClass, int nFieldIndex, bool bQuiet, void *pEntity)
{
	// other code
	if (pSendProp->var_name() == "m_vecViewOffset[2]" && Entity->m_nEntity == entityID)
	{
		isCrouchEvent = true;
	}
	
	//function continues...
```

We check if the value has already been initialized. Then, if `m_vecViewOffset[2]` is < 64.062561f (standing-state) and it the first time the player is crouching (and it is not a value in between the crouching event) we print out `printf("Action %d player_crouch %f %f %f \n", currentTick, playerPositionX, playerPositionY, playerPositionZ)`, which seamlessly simulates a crouch event. Else, if the player was crouched and it is now standing (`m_vecViewOffset[2]` == 64.062561f) we assert that the player is now in standing-state.

```
	//...here
	
	if (isCrouchEvent)
	{
		if (pResult->m_value.m_float != 0.000000f) // if the value has already been initialized
		{
			if (pResult->m_value.m_float < 64.062561f && !isPlayerCrouched) 
			{ 
				isPlayerCrouched = true; 
				printf("Action %d player_crouch %f %f %f \n", currentTick, playerPositionX, playerPositionY, playerPositionZ);
			}
			else if (pResult->m_value.m_float == 64.062561f && isPlayerCrouched)
			{
				isPlayerCrouched = false;
			}
}			
```

This is the easiest way of logging a crouch_event. 

We came up with a different way of doing it, by differenciating partial crouches and full crouches.

We basically check for then first time m_vecViewOffset[2] lowers after a standing-state, and we define this behaviour as `player_crouch_init`. Then we check for m_vecViewOffset[2] to lower again down to 46.044968f, which is a full crouch, defined as `player_crouch_full`.

```
if (pResult->m_value.m_float == 64.062561f) {
	isPlayerCrouched = false;
	printf("PlayerStanding, setCrouchToFalse\n");
}

if (pResult->m_value.m_float < 64.062561f && !isPlayerCrouched)
{
	printf("Action %d player_crouch_init %f %f %f %f\n", currentTick, playerPositionX, playerPositionY, playerPositionZ, pResult->m_value.m_float);
	isPlayerCrouched = true;
}
else if (pResult->m_value.m_float == 46.044968f)
{
	printf("Action %d player_crouch_full %f %f %f %f\n", currentTick, playerPositionX, playerPositionY, playerPositionZ, pResult->m_value.m_float);
	isPlayerCrouched = true;
}
```

Note that this is very error-prone. Indeed, checking in the output, sometimes we get:

```
OK : Action 128976 player_crouch_init 294.492950 653.842590 20.064556 63.311829
OK : Action 129000 player_crouch_full 294.492950 653.842590 20.064556 46.044968
WRONG! : Action 129260 player_crouch_init 295.996918 654.045227 33.935287 46.044968        <------------------
```
Originally, the values changed as follows:

```
63.311829 -> initiates crouching
46.044968 -> full crouch
64.062561 -> standing
46.044968 -> full crouch without an init as there is no intermediate state!
```

As you can see, 46.044968 should be considered a full crouch event, but it isn't. This is because the player crouches down, stands up, and then crouches down again. The second time though, `m_vecViewOffset[2]` goes immediately from 64.062561f to 46.044968, and as this happens pretty much in a single variation, the parser will interpret as a `player_crouch_init`. 

As the dataset will be used to train an Artificial Intelligence, we thought that dumping potentially wrong data in favour of more raw information was not worth it. We decided to comment out this last way of logging crouch events, in case you want to check it out.


**Formatting the *Entity* Output as Required**

Entities are not logged in complete bursts, dumping every table entry each tick. Indeed, demoinfogo deals with them with *Deltas*: this is to say that it only logs them when they change values.

From [this research paper](https://www.researchgate.net/publication/318873037_Data_Preprocessing_of_eSport_Game_Records_-_Counter-Strike_Global_Offensive) from Charles University, Prague, we found out that "*Each entity in the game is represented by its own structure (e.g., a player has a structure which contains coordinates on the map, pitch, health, etc.). Delta changes basically forms an update transaction of these structures – i.e., a list of game objects andtheir properties which should be inserted, updated, or removed from the game. Delta changes are much more complex to process as they do not carry a complete information, but only a change from the previous state.*" Therefore, to process the state of the game completely, we firstly had to gather all the data, store them and refresh them when it changed, as implied in the paper itself.

In order to format the output in the form of: 

```
Entity currentTick, mouseCoordX, mouseCoordY, playerPositionX, playerPositionY, playerPositionZ, playerVelocityX, playerVelocityY, playerVelocityZ
```

we decided to add to `GlobalPlayerInfo.h` those variables, making them conveniently accessible from everywhere in the parser.

```
// Player Entity-Event Info
extern double mouseCoordX;
extern double mouseCoordY;

extern double playerPositionX;
extern double playerPositionY;
extern double playerPositionZ;

extern double playerVelocityX;
extern double playerVelocityY;
extern double playerVelocityZ;


// Tick count
extern int currentTick;
```

As those variables are decoded and printed in `DecodePropWithEntity()`, we modified it to update the variables in `GlobalPlayerInfo.h`, instead of printing them directly.

```
Prop_t *DecodePropWithEntity(CBitRead &entityBitBuffer, FlattenedPropEntry *pFlattenedProp, uint32 uClass, int nFieldIndex, bool bQuiet, void *pEntity)
{
	//other code
	
	if (hasToRefresh)
	{
		if (pSendProp->var_name() == "m_vecVelocity[0]")
		{
			playerVelocityX = pResult->m_value.m_float;
		}

		if (pSendProp->var_name() == "m_vecVelocity[1]")
		{
			playerVelocityZ = pResult->m_value.m_float;
		}

		if (pSendProp->var_name() == "m_vecVelocity[2]")
		{
			playerVelocityY = pResult->m_value.m_float;
		}

		if (pSendProp->var_name() == "m_vecOrigin")
		{
			playerPositionX = pResult->m_value.m_vector.x;
			playerPositionY = pResult->m_value.m_vector.y;
		}
		if (pSendProp->var_name() == "m_vecOrigin[2]")
		{
			playerPositionZ = pResult->m_value.m_float;
		}
		if (pSendProp->var_name() == "m_angEyeAngles[0]")
		{
			mouseCoordY = pResult->m_value.m_float;
		}
		if (pSendProp->var_name() == "m_angEyeAngles[1]")
		{
			mouseCoordX = pResult->m_value.m_float;
		}

	}
	
	// other code
}
```


In the `bool ReadNewEntity( CBitRead &entityBitBuffer, EntityEntry *pEntity )` function, when the `DT_CSPlayer` table is read,  we let `DecodePropWithEntity()` update the values and when the `DT_CSPlayer` entityID matches the target player's entityID we print out the data.

```
bool ReadNewEntity( CBitRead &entityBitBuffer, EntityEntry *pEntity )
{
	// other code
	
	if (pTable->net_table_name() == "DT_CSPlayer" && pEntity->m_nEntity == entityID)
	{
		printf("Entity %d %f %f %f %f %f %f %f %f %f %f \n", currentTick,
								     mouseCoordX,
								     mouseCoordY,
								     playerPositionX,
								     playerPositionY,
								     playerPositionZ,
								     playerVelocityX,
								     playerVelocityY,
								     playerVelocityZ);
	}
	
	// other code
}
```

During testing multiple demos, we found out that in the `void CDemoFileDump::DoDump()` function called in `main()`, the parser reads a command from the demo header, and handles it via a `switch`. More information on the `DEM` format [here](https://developer.valvesoftware.com/wiki/DEM_Format).

Not all demos ever enter in the `dem_stringtables` switch case, causing `DumpStringTables()` to never be called.

```
case dem_stringtables:
{
	char *data = ( char * )malloc( DEMO_RECORD_BUFFER_SIZE );
	CBitRead buf( data, DEMO_RECORD_BUFFER_SIZE );
	m_demofile.ReadRawData( ( char* )buf.GetBasePointer(), buf.GetNumBytesLeft() );
	buf.Seek( 0 );
	if ( !DumpStringTables( buf ) )
	{
		printf( "Error parsing string tables. \n" );
	}
	free( data );
}
break;

```

The parser would enter in the `dem_packet` switch case instead.

```
case dem_packet:
{
	HandleDemoPacket();
}
break;	
```

This results in the parser not ever setting the global player variables,  causing no output in the log.

In order to understand what was happening, we decided to follow the call stack of the parser, starting from `HandleDemoPacket()`. The latter calls `DumpDemoPacket()`, as follows:

```
void CDemoFileDump::HandleDemoPacket()
{
	//other code

	DumpDemoPacket( buf, length );
}
```

`DumpDemoPacket()` has its own switch, and defines a macro for the `PrintNetMessage()` function for each command.


```
void CDemoFileDump::DumpDemoPacket( CBitRead &buf, int length )
{
	//other code

	switch( Cmd )
	{
	   #define HANDLE_NetMsg( _x )	case net_ ## _x: PrintNetMessage< CNETMsg_ ## _x, net_ ## _x >( *this, buf.GetBasePointer() + buf.GetNumBytesRead(), Size ); break
	   #define HANDLE_SvcMsg( _x )	case svc_ ## _x: PrintNetMessage< CSVCMsg_ ## _x, svc_ ## _x >( *this, buf.GetBasePointer() + buf.GetNumBytesRead(), Size ); break

		default:
			// unknown net message
			break;

		HANDLE_NetMsg( NOP );            	// 0
		HANDLE_NetMsg( Disconnect );        // 1
		HANDLE_NetMsg( File );              // 2
		HANDLE_NetMsg( Tick );              // 4
		HANDLE_NetMsg( StringCmd );         // 5
		HANDLE_NetMsg( SetConVar );         // 6
		HANDLE_NetMsg( SignonState );       // 7
		HANDLE_SvcMsg( ServerInfo );        // 8
		HANDLE_SvcMsg( SendTable );         // 9
		HANDLE_SvcMsg( ClassInfo );         // 10
		HANDLE_SvcMsg( SetPause );          // 11
		HANDLE_SvcMsg( CreateStringTable ); // 12
		HANDLE_SvcMsg( UpdateStringTable ); // 13
		HANDLE_SvcMsg( VoiceInit );         // 14
		HANDLE_SvcMsg( VoiceData );         // 15
		HANDLE_SvcMsg( Print );             // 16
		HANDLE_SvcMsg( Sounds );            // 17
		HANDLE_SvcMsg( SetView );           // 18
		HANDLE_SvcMsg( FixAngle );          // 19
		HANDLE_SvcMsg( CrosshairAngle );    // 20
		HANDLE_SvcMsg( BSPDecal );          // 21
		HANDLE_SvcMsg( UserMessage );       // 23
		HANDLE_SvcMsg( GameEvent );         // 25
		HANDLE_SvcMsg( PacketEntities );    // 26
		HANDLE_SvcMsg( TempEntities );      // 27
		HANDLE_SvcMsg( Prefetch );          // 28
		HANDLE_SvcMsg( Menu );              // 29
		HANDLE_SvcMsg( GameEventList );     // 30
		HANDLE_SvcMsg( GetCvarValue );      // 31

		#undef HANDLE_SvcMsg
		#undef HANDLE_NetMsg
	}

	//other code
}
```


`PrintNetMessage()` is a templated function which has lots of definitions. In one of the many, `ParseStringTableUpdate()` is called:

```
template <>
void PrintNetMessage< CSVCMsg_CreateStringTable, svc_CreateStringTable >( CDemoFileDump& Demo, const void *parseBuffer, int BufferSize )
{
	// other code
	
	CBitRead data( &msg.string_data()[ 0 ], msg.string_data().size() );
	
	ParseStringTableUpdate( data,  msg.num_entries(), msg.max_entries(), msg.user_data_size(), msg.user_data_size_bits(), msg.user_data_fixed_size(), bIsUserInfo );
	
	// other code
}
```

`ParseStringTableUpdate()` has something in common with the original `DumpStringTable()` function.

```
void ParseStringTableUpdate( CBitRead &buf, int entries, int nMaxEntries, int user_data_size, int user_data_size_bits, int user_data_fixed_size, bool bIsUserInfo )
{
	//other code
	
	if ( bIsUserInfo && pUserData != NULL )
	{
		const player_info_t *pUnswappedPlayerInfo = ( const player_info_t * )pUserData;
		player_info_t playerInfo = *pUnswappedPlayerInfo;  					// -----> that's the playerInfo structure
		playerInfo.entityID = entryIndex;							// -----> that's the entityID

		LowLevelByteSwap( &playerInfo.xuid, &pUnswappedPlayerInfo->xuid );
		LowLevelByteSwap( &playerInfo.userID, &pUnswappedPlayerInfo->userID );
		LowLevelByteSwap( &playerInfo.friendsID, &pUnswappedPlayerInfo->friendsID );

		bool bAdded = false;
		auto existing = FindPlayerByEntity(entryIndex);  					
		if ( !existing ) 
		{
			bAdded = true;
			s_PlayerInfos.push_back(playerInfo);
		}
		else {
			*existing = playerInfo;
		}
		
		//other code
	}	
}
```
This basically offers us another chance to set our own player variables. Indeed, we have the whole `player_info_t playerInfo` as before, as well as the Entity Entry index, which is the entityID.

Therefore, we just added:

```
if (playerInfo.xuid == targetPlayerSteamID)
{
	userID = playerInfo.userID;
	entityID = playerInfo.entityID;
}
```
After setting the `entityID` and `userID` variables, the parser could now retrieve them and check them out in the `if()` statements, thus letting the parser print out the information from `ReadNewEntity()` as it should.

## Parser Output Documentation

The Parser Output is not very straight-forward to understand, expecially when it comes to game events' additional information. The complete documentation of the Parser's output format is [here](https://github.com/marcouderzo/CSDemoParser/blob/main/documentation/ParserFormat_Documentation.md). 


## Automating the Parsing of the Match Pool

### autoparse.py

As the match pool is very large, parsing every match manually is just not feasable. So, we decided to write a simple script to automate the parsing process.

You can read the documentation on how it works in detail [here](https://github.com/marcouderzo/CSDemoParser/blob/main/documentation/autoparse%20Script%20Documentation.md)


## Dataset Validation Testing

### validatedataset.py

Testing and validating the dataset is always a good practice. We decided to write a simple but very effective script that does it.

You can read the documentation on the tests we decided to run [here](https://github.com/marcouderzo/CSDemoParser/blob/main/documentation/validateoutput%20Script%20Documentation.md)
