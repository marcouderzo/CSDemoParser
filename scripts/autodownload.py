from selenium import webdriver
import re
import os
import time as t
from pyunpack import Archive
import json

# link: https://www.hltv.org/stats/players/matches/...

# #profileLink = "https://www.hltv.org/stats/players/matches/11893/zywoo"

def download(path, innerLink):

    global downloaded
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

    dlname=""

    for file in os.listdir("C:/Users/samuk/Downloads"):
        if file.endswith(".crdownload"):
            dlname = file

    targetfile = 'C:/Users/samuk/Downloads/' + dlname
    print(targetfile)

    hasDownloaded = False

    while not hasDownloaded:
        t.sleep(2)
        if not os.path.exists(targetfile):
            hasDownloaded = True

    print("Download done")

    downloaded = downloaded + 1

    downloadingDriver.close()

    finalDriver.close()







def goToDownloadPage(path, link, nextLink):
    """
        Funzione che scarica il singolo replay
        Apre una nuova finestra del browser e va al link passato come parametro. Poi cerca il link giusto tramite il
        parametro nextLink. Una volta trovato va al link e scarica il replay
    """

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
        # /matches/2335421/youngsters-vs-heretics-lootbet-season-3
        if type(innerLink).__name__ != "NoneType" and innerLink.find("/matches/") > 0 and nextLink in innerLink:
            print("Ci entro")
            if "?" not in innerLink:

                print("InnerLink {}".format(innerLink))
                download(path, innerLink)
                break

    innerDriver.close()






def takePlayerMatches(path, profileLink, playerNamePar):
    """
        Questa funzione prende il link del profilo di un giocatore (che viene passato dal chiamante) e scarica 100
        partite del giocatore di cui gli viene passato il link del profilo.
        Si avvale di un'altra funzione
        è possibile che bisogni specificare i percorsi di Firefox e Chrome anche se non dovrebbe essere necessario
     """

    global downloaded
    downloaded = 0
    listOfMatch = []

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])

    driver = webdriver.Chrome(path, options=chrome_options)
    driver.get(profileLink)

    print("First driver set")

    # driver.maximize_window()

    table = driver.find_elements_by_class_name("stats-table")
    print("Length of table {}".format(str(len(table))))
    resultTd = table[0].find_elements_by_tag_name("td")
    print("First td text {}".format(resultTd[0].text))

    prev = ''
    i = 0


    while downloaded < 3:
        # aux conta gli elementi td. Interessano il primo, il secondo e il terzo di ogni riga
        # (i nomi dei team e la data della partita).
        # Ci sono 7 colonne nella tabella
        aux = 7 * i
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
            print("Scaricato il {} file".format(str(downloaded) + "°"))
            listOfMatch.append(playerNamePar + "_" + str(downloaded))
            prev = nextLink
        i = i + 1



    print(listOfMatch)
    driver.close()
    dizionario[playerNamePar] = listOfMatch


















































































path = 'C:/Program Files (x86)/Google/Chrome/Application/chromedriver.exe'

canc = input("Vuoi cancellare i file .rar alla fine dello script?")
dizionario = {}

#Prendo tutti i link dal file Players.txt
f = open("Players.txt")

playerName = []

downloaded = 0

for x in f:
    stringAux = str(x)
    print(stringAux)
    lastIndex = stringAux.rfind("/")
    playerName.append(stringAux[lastIndex + 1 : ])
    print(stringAux[lastIndex + 1 : ])
    takePlayerMatches(path, str(x), playerName[len(playerName)-1])
    print(playerName)

f.close()

jsonDump = json.dumps(dizionario)
with open("MatchesDict.json", "w") as outfile:
    outfile.write(jsonDump)

#Faccio l'unrar di tutti i file in un'apposita sottocartella
pathOfScript = 'C:/Users/marco/Desktop/pyscript/dl'
i = 0
for entry in os.scandir(pathOfScript):
    if entry.is_file() and entry.path.endswith('.rar'):
        pathToExtract = path + '/tmp/'
        os.rename(pathToExtract + entry.__name__, playerName[i / 100] + "_" +str (i % 100 + 1))
        i = i + 1
        Archive(entry.path).extractall(pathToExtract, auto_create_dir = True)

# elimino i file .rar
if canc == "Si" or canc == "si":
    for entry in os.scandir(pathOfScript):
        if entry.is_file() and entry.path.endswith('.rar'):
            os.remove(entry.path)
