import os, subprocess
import json

# -------Setup----------

demospath = "F:/progetto/dem_awaitingcheck"        # Where are your demos
logpath = "F:/progetto/log"          # Where are your logs

jsonDict = "MatchesDict.json"        # JSON Dictionary of Matches to import

lineThreshold = 100000               # Minimum number of lines in the log.

# ---------------------


SteamID_dict = {  'pashabiceps': [76561197973845818],
             'flusha': [76561197991348083, 76561198117206736],
             'jw': [76561198031554200],
             'krimz': [76561198031651584],
             'olofmeister': [76561197988627193],
             'karrigan': [76561197989430253],
             'device': [76561197987713664],
             'gla1ve': [76561198010511021],
             'xyp9x': [76561197990682262, 76561198116400733],
             'dupreeh': [76561198004854956],
             'electronic': [76561198044045107],
             'flamie': [76561198116523276],
             's1mple': [76561198034202275, 76561198298306246],
             'shox': [76561198006920295],
             'smithzz': [76561197974587647, 76561197962060457, 76561198267915276],
             'kennys': [76561197987883012, 76561198406770456, 76561198364448565],
             'aleksib': [76561198013243326, 76561198073116389],
             'coldzera': [76561198039986599],
             'fallen': [76561197960690195],
             'fer': [76561197999186947],
             'liazz': [76561198072321716],
             'niko': [76561198041683378],
             'twistzz': [76561198016255205],
             'guardian': [76561197972331023],
             'olivia': [76561198061745802],
             'floppy': [76561198306519263],
             'moose': [76561198078144931, 76561198324395878],
             'get-right': [76561197982036918],
             'k0nfig': [76561197979669175, 76561198069730996],
             'twist': [76561197980244859, 76561198147205437],
             'snatchie': [76561197981967565],
             'fox': [76561197962205264, 76561198094086500],
             'chrisj': [76561198223789184, 76561197988539104],
             'n0thing': [76561197961021014],
             'adren': [76561197961631761, 76561198006466707],
             'hazed': [76561197990571509, 76561197999248947],
             'pyth': [76561198017578295],
             'freakazoid': [76561197977148799, 76561198030919062],
             'neo': [76561197960725934],
             'lambert': [76561197960282565],
             'arya': [76561197960677505],
             'zeus': [76561198019328472, 76561198129539354],
             'taz': [76561197960499780],
             'lex': [76561197962957566, 76561197973133888],
             'crush': [76561197997247152],
             'krystal': [76561197977791735],
             'golden': [76561198076775225],
             'taco': [76561198013142296, 76561198275584267],
             'coffee': [76561198206916976],
             'voltage': [76561198047129384],

             }


file = open(jsonDict, 'r')
Matches_dict = json.load(file)
# print(Matches_dict)
file.close()

#nel dizionario di giocatori con relative partite, per ogni giocatore parsa tutte le sue partite, cercando ad 
#ogni parsing il nome del giocatore (comune ai due dizionari) e prova tutti gli steamid del giocatore 



generalErroredParsings= []
steamIDFailedParsings= []
needCheckParsings = []
tooBriefLogs = []
exitCode3Parsings = []

knownExitCodes = [1, 2, 3, 3221226505]

os.chdir("..")
os.chdir("parser")

for player in Matches_dict.items(): #for each player
    # print(player)
    for match in player[1]: #take every match of that player
        # print(match)
        for file in os.listdir(demospath): #in the demospath folder

            if file.endswith(".dem") and file == match: #check for that match
                print("Parsing " + file)
                demofile = os.path.join(demospath, file).replace("\\", "/")
                #print(demofile)
                success = False
                for s_player in SteamID_dict.items(): #for each possible SteamID of that player, try parsing the match
                    if s_player[0] == player[0]:
                        for intSteamID in s_player[1]:

                            SteamID = str(intSteamID)
                            p = subprocess.run(["demoinfogo", SteamID , demofile])

                            hasFailedWithSteamIDs=False
                            hasExitedUnexpectedly=False

                            if(p.returncode == 2): #failed, for loop continues with next steamID, if present.
                                print("     -> No such SteamID in this match, retrying with next SteamID...")
                                hasFailedWithSteamIDs=True
                                continue
                            if(p.returncode == 1): #succeded, break the for loop and go on with next file
                                print("     -> Parsed Successfully.")
                                success = True
                                hasFailedWithSteamIDs=False
                                break
                            if(p.returncode == 3): #fatal error at end of demo, dump is still successful
                                print("     -> Parsed Successfully. (*ExitCode3)")
                                templog = file.replace(".dem", ".txt")
                                logfile = logpath + '/' + templog
                                with open(logfile, "r+", encoding = "utf-8") as lfile:
                                    line_count = 0
                                    for line in lfile:
                                        line_count += 1
                                if line_count < lineThreshold:
                                    tooBriefLogs.append(lfile)  
                                    if line_count == 0:
                                        print("     -> Empty Log")
                                    else:    
                                        print("     -> Low line count. Please check the logfile lenght!")     
                                exitCode3Parsings.append(file)
                                success = True
                                hasFailedWithSteamIDs=False
                                break
                            if(p.returncode == 3221226505): #stack overflow at end of demo, dump is still successful
                                print("     -> Overflow error.")
                                templog = file.replace(".dem", ".txt")
                                logfile = logpath + '/' + templog
                                with open(logfile, "r+", encoding = "utf-8") as lfile:
                                    line_count = 0
                                    for line in lfile:
                                        line_count += 1
                                    lfile.seek(0, os.SEEK_END)
                                    pos = lfile.tell() - 1
                                    while pos > 0 and lfile.read(1) != "\n":
                                        pos -= 1
                                        lfile.seek(pos, os.SEEK_SET)
                                    if pos > 0:
                                        lfile.seek(pos, os.SEEK_SET)
                                        lfile.truncate()
                                print("     -> Erased last line.")
                                if line_count < lineThreshold:
                                    tooBriefLogs.append(lfile)
                                    if line_count == 0:
                                        print("     -> Empty Log")
                                    else:    
                                        print("     -> Low line count. Please check the logfile lenght!")
                                        
                                else:
                                    print("     -> Parsed Successfully. (*StackOverflow)")
                                    needCheckParsings.append(logfile)
                                    success = True
                                    hasFailedWithSteamIDs=False                
                                break
                            
                            if p.returncode not in knownExitCodes:
                                print("     -> Unexpected Exit Code: " + str(p.returncode))
                                hasExitedUnexpectedly=True
                                break

                if not success and hasFailedWithSteamIDs: #if failed with every SteamID in dictionary, save the match name for later report.
                    print("     -> Could not find the target player with any of the SteamIDs! Check the report later.")
                    steamIDFailedParsings.append(file)
                if not success and hasExitedUnexpectedly: #if failed with every SteamID in dictionary, save the match name for later report.
                    print("     -> Could not parse this match (Unexpected Exit Code)! Check the report later.")
                    generalErroredParsings.append(file)
                    

print("--------REPORT--------")

if generalErroredParsings:
    print("Could not parse some matches. Reason: Unexpected Exit Code: ", generalErroredParsings)
if steamIDFailedParsings:
    print("Could not parse some matches. Reason: Unable to Find SteamID: ", steamIDFailedParsings)
if tooBriefLogs:
    print("Could not parse some matches. Reason: Log Seems Too Brief: ", tooBriefLogs)

else:
    print("Done parsing match pool. No errors occurred.")

print("")

if needCheckParsings:
    print("Stack Overflows - Handled Successfully in: ", needCheckParsings)
if exitCode3Parsings:
    print("Exit Code 3 - Handled Successfully in: ", exitCode3Parsings)  

