from selenium import webdriver
from pyunpack import Archive
import re
import os
import time as t
import json
import shutil
import patoolib

# link: https://www.hltv.org/stats/players/matches/...



# #profileLink = "https://www.hltv.org/stats/players/matches/11893/zywoo"

def delete():
    global pathOfDownload
    for entry in os.scandir(pathToMove):
        if entry.is_file() and entry.path.endswith('.rar'):
            os.remove(entry.path)


def rename(path):
    global currentPlayerName
    global downloaded
    global listOfMatch
    global playerName

    for entry in os.scandir(path):
        alreadyPresent = False
        if entry.is_file() and entry.path.endswith('.dem'):
            for x in playerName:
                if x in entry.path:
                    alreadyPresent = True

            if alreadyPresent == False:
                os.rename(entry, path + currentPlayerName + '_' + str(downloaded + 1) + '.dem')
                listOfMatch.append(currentPlayerName + '_' + str((downloaded + 1)) + '.dem')
                print("Ci sono entrato finalmente {}".format(downloaded))
                downloaded = downloaded + 1
    delete()

def unpack():
    pathofRar="D:/progetto/"

    print(pathofRar)
    i = 0
    for entry in os.scandir(pathofRar):
        if entry.is_file() and entry.path.endswith('.rar'):
            print(str(i))
            pathToExtract = pathofRar + 'tmp/'
            print(pathToExtract)
            i = i + 1
            Archive(entry.path).extractall(pathToExtract, auto_create_dir=True)
    rename(pathToExtract)


def move():
    global pathOfDownload
    global pathToMove

    fileName = ''

    for entry in os.scandir(pathOfDownload):
        if entry.is_file() and entry.path.endswith('.rar'):
            fileName = entry.path[entry.path.rfind('/') + 1:]
            shutil.move(entry.path, pathToMove + fileName)

    unpack()


def download(path, innerLink):
    global downloaded
    global pathOfDownload

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])

    finalDriver = webdriver.Chrome(path, options=chrome_options)
    finalDriver.get(innerLink)

    print("Third driver done")

    box = finalDriver.find_elements_by_class_name("stream-box")
    link = box[0].find_elements_by_tag_name("a")[0].get_attribute("href")

    print("RealLink {}".format(link))

    downloadingDriver = webdriver.Chrome(path, options=chrome_options)
    downloadingDriver.get(link)

    print("Fourth driver done")

    t.sleep(20)

    dlname = ""
    print("waited 20 seconds hard coded")
    for file in os.listdir(pathOfDownload):
        print("there is a file: "+file)
        if file.endswith(".crdownload"):
            print("recognizes there's a crdownload")
            dlname = file

    targetfile = pathOfDownload + dlname
    print(targetfile)

    hasDownloaded = False
    print("before waiting")
    while not hasDownloaded:
        t.sleep(2)
        if not os.path.exists(targetfile):
            hasDownloaded = True
    print("waited")
    print("Download done")

    downloadingDriver.close()
    finalDriver.close()

    print("beforemoving")
    move()
    print("hasmoved")





def goToDownloadPage(path, link, nextLink):

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])

    innerDriver = webdriver.Chrome(path, options=chrome_options)
    innerDriver.get(link)

    print("Second driver done")

    innerResult = innerDriver.find_elements_by_tag_name("a")
    print("InnerResultLength {}".format(len(innerResult)))

    for x in innerResult:

        innerLink = x.get_attribute("href")
        if x.get_attribute("class") == "match-page-link button":
            print("InnerLink {}".format(innerLink))
            download(path, innerLink)
            break

    innerDriver.close()

def takePlayerMatches(path, profileLink, playerNamePar):

    global pathOfDownload
    global downloaded
    global listOfMatch
    downloaded = 0
    listOfMatch = []

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])

    driver = webdriver.Chrome(path, options=chrome_options)
    driver.get(profileLink)

    print("First driver set")

    prev = ''
    i = 0

    while downloaded < 100:

        table = driver.find_elements_by_class_name("stats-table")
        print("Length of table {}".format(str(len(table))))
        resultTd = table[0].find_elements_by_tag_name("td")
        print("First td text {}".format(resultTd[0].text))

        # aux conta gli elementi td. Interessano il primo, il secondo e il terzo di ogni riga
        # (i nomi dei team e la data della partita).
        # Ci sono 7 colonne nella tabella
        print("downloaded {}".format(downloaded))
        aux = 7 * i
        print(str(i))
        print(str(aux))
        # resultA contiene tutti i link figli del td corrente e che sono dei link. Questo si riduce a un solo elemento
        # per ogni td, però essento il risultato inserito in una lista bisogna comunque selezionare il primo elemento
        resultA = resultTd[aux].find_elements_by_tag_name("a")[0]
        print("Type {}".format(type(resultA)))
        print("result {}".format(resultA))
        print("text {}".format(resultA.text))
        print("href {}".format(resultA.get_attribute("href")))

        team = resultTd[aux + 1].text
        # Dopo il nome del team c'è uno spazio seguito da un numero tra parentesi. Le 3 linee seguenti servono a
        # togliere questi caratteri, con l'accortezza che bisogna rimuovere solo gli spazi e i numeri che compaiono
        # alla fine
        team = re.sub(" (\([0-9]+\))", "", team)
        team = team.replace(" ", "-")
        team = team.lower()
        print("Team {}".format(team))

        enemyTeam = resultTd[aux + 2].text
        # rimozione dei caratteri analoga alla precedente
        enemyTeam = re.sub(" (\([0-9]+\))", "", enemyTeam)
        enemyTeam = enemyTeam.replace(" ", "-")
        enemyTeam = enemyTeam.lower()
        print("EnemyTeam {}".format(enemyTeam))

        nextLink = "/" + team + "-vs-" + enemyTeam
        print("NextLink {}".format(nextLink))

        if nextLink != prev:
            goToDownloadPage(path, resultA.get_attribute("href"), nextLink)
            print("Scaricato il {} archivio".format(str(i) + "°"))
            prev = nextLink

        driver.refresh()

        print("Refreshed")
        i = i + 1

    print(listOfMatch)
    driver.close()
    dizionario[playerNamePar] = listOfMatch
    jsonDump = json.dumps(dizionario)
    with open("MatchesDict.json", "a") as outfile:
        outfile.write(jsonDump)



########################################################################################################################
########################################################################################################################
########################################################################################################################


path = 'C:/Users/marco/Desktop/chromedriver.exe'
pathOfDownload = 'C:/Users/marco/Downloads/'
pathToMove = "D:/progetto/"

listOfMatch = []

dizionario = {}

#Prendo tutti i link dal file Players.txt
f = open("Players.txt")

playerName = []

downloaded = 0
currentPlayerName = ''

for x in f:
    stringAux = str(x)
    print(stringAux)
    lastIndex = stringAux.rfind("/")
    currentPlayerName = stringAux[lastIndex + 1 : len(stringAux) - 1]
    playerName.append(currentPlayerName)
    print("Current player {}".format(currentPlayerName))
    takePlayerMatches(path, str(x), currentPlayerName)
    print(playerName)

f.close()

#Faccio l'unrar di tutti i file in un'apposita sottocartella