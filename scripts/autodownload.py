from selenium import webdriver
import re
import os
from pyunpack import Archive

# link: https://www.hltv.org/stats/players/matches/...

# #profileLink = "https://www.hltv.org/stats/players/matches/11893/zywoo"

def download(path, innerLink):

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])

    finalDriver = webdriver.Chrome(path, options=chrome_options)
    finalDriver.get(innerLink)

    box = finalDriver.find_elements_by_class_name("stream-box")
    link = box[0].find_elements_by_tag_name("a")[0].get_attribute("href")

    downloadingDriver = webdriver.Chrome(path, options=chrome_options)
    downloadingDriver.get(link)

    #downloadingDriver.close()
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

    innerResult = innerDriver.find_elements_by_tag_name("a")

    for x in innerResult:

        innerLink = x.get_attribute("href")
        # /matches/2335421/youngsters-vs-heretics-lootbet-season-3
        if type(innerLink).__name__ != "NoneType" and innerLink.find("/matches/") > 0 and nextLink in innerLink:
            if "?" not in innerLink:

                download(path, innerLink)

    innerDriver.close()

def takePlayerMatches(path, profileLink):
    """
        Questa funzione prende il link del profilo di un giocatore (che viene passato dal chiamante) e scarica 100
        partite del giocatore di cui gli viene passato il link del profilo.
        Si avvale di un'altra funzione
        è possibile che bisogni specificare i percorsi di Firefox e Chrome anche se non dovrebbe essere necessario
     """

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])

    driver = webdriver.Chrome(path, options=chrome_options)
    driver.get(profileLink)

    # driver.maximize_window()

    table = driver.find_elements_by_class_name("stats-table")
    #print(str(len(table)))
    resultTd = table[0].find_elements_by_tag_name("td")
    #print(resultTd[0].text)

    prev = ''
    i = 0

    while i < 100:
        # aux conta gli elementi td. Interessano il primo, il secondo e il terzo di ogni riga
        # (i nomi dei team e la data della partita).
        # Ci sono 7 colonne nella tabella
        aux = 7 * i
        # resultA contiene tutti i link figli del td corrente e che sono dei link. Questo si riduce a un solo elemento
        # per ogni td, però essento il risultato inserito in una lista bisogna comunque selezionare il primo elemento
        resultA = resultTd[aux].find_elements_by_tag_name("a")[0]
        # print(type(resultA))
        # print(resultA)
        # print(resultA[0].text)
        # print(resultA[0].get_attribute("href"))
        # print(str(len(resultA)))

        team = resultTd[aux + 1].text
        # Dopo il nome del team c'è uno spazio seguito da un numero tra parentesi. Le 3 linee seguenti servono a
        # togliere questi caratteri, con l'accortezza che bisogna rimuovere solo gli spazi e i numeri che compaiono
        # alla fine
        team = re.sub(" (\([0-9]+\))", "", team)
        team = team.lower()
        #print(team)

        enemyTeam = resultTd[aux + 2].text
        # rimozione dei caratteri analoga alla precedente
        enemyTeam = re.sub(" (\([0-9]+\))", "", enemyTeam)
        enemyTeam = enemyTeam.lower()
        #print(enemyTeam)

        nextLink = "/" + team + "-vs-" + enemyTeam
        #print(nextLink)
        if nextLink != prev:
            goToDownloadPage(path, resultA.get_attribute("href"), nextLink)
            print("Scaricato il {} file".format(str(i + 1) + "°"))
        i = i + 1

    driver.close()


path = 'C:/Users/marco/AppData/Local/Google/Chrome/Application/chromedriver.exe'

#download('https://www.hltv.org/matches/2335421/youngsters-vs-heretics-lootbet-season-3')
#takePlayerMatches(path, "https://www.hltv.org/stats/players/matches/317/pashabiceps")

#Prendo tutti i link dal file Players.txt
f = open("Players.txt")

for x in f:
    takePlayerMatches(path, str(x))

f.close()

#Faccio l'unrar di tutti i file in un'apposita sottocartella
pathOfScript = 'C:/Users/marco/Desktop/pyscript/dl'
i = 1
for entry in os.scandir(pathOfScript):
    if entry.is_file() and entry.path.endswith('.rar'):
        pathToExtract = path + '/tmp/' + str(i)
        i = i + 1
        Archive(entry.path).extractall(pathToExtract, auto_create_dir = True)

#elimino i file .rar

# for entry in os.scandir(pathOfScript):
#     if entry.is_file() and entry.path.endswith('.rar'):
#
#         os.remove(entry.path)