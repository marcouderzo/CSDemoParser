# How it works
The script is divided in 3 different parts: the download part, the unrar part and the delete part.

## Prerequisites
There is a list of prerequisites for the script:
- Since the script is written in Python, python is needed. Note that is needed a 3.5+ version
- The script assumes the user has Chrome installed
- The script uses some modules. Some of them (re, os and time) are part of standard Python. The others (selenium and pyunpack) need to be downloaded if not already present. iNote that the script does not import all selenium and all pyunpack, only selenium.webdriver and pyunpack.Archive
  
## How it works
This is the first part of the script, it is set to download all the 5000 matches. This part needs a file called Players.txt which contains all the links to the hltv.org page of the players you want the mathces of. Note that
this file must contain only one link for each line and has to end with an empty last line, so you have to write the links and go to a new line.
The script proceeds to open the file, take the links with a for loop and take the name of the player from the link. Then it opens a chrome window and goes to the player page.
Once it's there it takes all the td elements of the table that has the class specified (it's the table that contains all the links to the matches). Every row of the table has 7 cells, and the first cell of every row contains
a link that refers a page with the details of the match. The second and the third cell contain the player's team's name and the enemy's team name. The script checks the player team name and the enemy team name, and if they 
are the same as the ones that were just donwloaded, the script skips the link. This is because there are some matches in which the teams play more than 1 match and downloading the first one via the link is enough to download
all of the matches. In order to make sure that the donwloaded matches are not duplicates, the script skips the links where enemy team and player team are the same as the one that have just been downloaded.
After finding a new link, the script opens it in a new Chrome window, then it goes to the download page and downloads the match performing a get request via the URL. Sice python is an asyncronous language, we had to use a
trick to let chrome download the file without the script closing the window before the end of the download. So the script downloads the file in the default directory (C:/Users/[currentUser]/Downloads/ on Windows), and creates
a temp file with the extension .CRDOWNLOAD. The script checks every 2 seconds if the file with that extension exists, and if it does, it waits. If the file does not exists anymore, the download finished and the script can close
the Chrome windows. 

Once the download finished, the scipt proceeds to unpack the .rar file that was donwloaded in a subdirectory called tmp. After doing this, it loops through all the files in the tmp directory searching for files with the .dem
extension that do not contain the name of one of the players whose match have already been already downloaded (meaning it finds the latest extracted files) and renames them with the standard playerName_numberOfTheMatch. Doing so
allows us to count the matches downloaded and stop the download for the current player if the number of matches is equal (or grater then) 100. Note that even if the number of needed matches is 100, it is possible that the script downloads
more then 100 matches for every player, for example if it has already downloaded 99 matches and the next .rar archive has 2 matches the number of downloaded matches is 101. Anyway, the script that attaches the matches just downloaded
to a list that will be attached to a dictionary at the end of the download for that player. This allows us to have a dictionary of the matches related to the player that will be dumped in a JSON file at the end of the script.

After the extraction, the script deletes from the disk the .rar file downloaded, since it would cause a problem because of the multiple extraction. In fact, the script extracts all .rar files it finds in the download directory,
and not removing a file would result in it being extraced multiple times and causing a miscalculation of the downloaded matches.
