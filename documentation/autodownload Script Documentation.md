# How it works
The script is divided in 3 different parts: the download part, the unrar part and the (optional) delete part.

## Prerequisites
There is a list of prerequisites for the script:
- Since the script is written in Python, python is needed. Note that is needed a 3.5+ version
- The script assumes the user has Chrome installed
- The script uses some modules. Some of them (re, os and time) are part of standard Python. The others (selenium and pyunpack) need to be downloaded if not already present. iNote that the script does not import all selenium and all pyunpack, only selenium.webdriver and pyunpack.Archive
  
## Download
This is the first part executed by the script. It downloads all the matches needed, for a total of 5000 matches. It takes a txt file, that must be called Players.txt which contains a list of links (each one on a new line) corresponding to the list of profiles of the players we want the matches of. with a simple for loop it iterates on the links. For each link it calls a function called takePlayerMatches. This function opens a Chrome window and gets the link of the player. In this page there is a table full of matches of the player. We already checked that each of this players has 100 or more matches. For each match it takes the names of the player's team and the name of the enemy team, used in the next step. Then takes the link of the match (on the first cell of each row) and, if the partial link found with the player's and enemy's team name is different from the previous one, calls another function called goToDownloadPage. This function gets the link of the match and opens a new Chrome window on that link. Then it scans all the links on the page until it finds a link which has the substring "/matches/", the partial link and does not contain "?". If all this checks are passed it means that the current link is the one that goes to the match details page. At this point the script calls another function, called download, which finally downloads the match. This function opens another Chrome window and gets the details match page. From this page the script gets the real download link in another Chrome window by getting the href attribute of the first of three boxes with a class called "stream-box". Here comes a tricky part of the script, because it does not autmatically wait for the download to finish, so there is a part which involves waiting (with time.sleep()) until the partial file ("That can be distinguished because of the .CRDOWNLOAD extension) is not present in the directory anymore. So there is a for cycle that cycles through all the files in the download directory until finds the .CRDOWNLOAD file, takes its name and with a while, every 2 seconds checks if the file still exists. If the file is present, the download didn't finish, so the script waits 2 more seconds, if the file is not present anymore the download finished and it can close the window without problems for the download. So it closes also the third window opened and the second one. The control reaches takePlayerMatches that proceeds with the next file. This process continues until 100 matches of the same player are downloaded. When the player has 100 matches, the control returns to the initial for cycle that proceeds with the next player.

## Unrar
This is the second part of the script. Since all the downloaded files are in .rar format, the script also unpacks the archives. For this operation it uses the os.scandir() and the pyunpack module. Basically, the script scans the download directory and unpacks every .rar file it finds in the /tmp/i directory, with i being a number between 1 and 5000. With this, every archive is unpacked in a different directory, to mantain all the files of the same archive (which may be multiple, usually 2 but sometimes more) united in the same directory.

## Delete
There is also a third part. This part is currently optional, so if the input the user insert at the beginning, when asked, is "Si" or "si" the script also deletes every .rar file found in the download directory. This operation requires Python 3.5+ and uses os.remove().