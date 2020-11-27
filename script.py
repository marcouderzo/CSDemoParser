from selenium import webdriver
from selenium.webdriver import FirefoxProfile
import re
import urllib
import urllib.request

# link: https://www.hltv.org/stats/players/matches/...

# #profileLink = "https://www.hltv.org/stats/players/matches/11893/zywoo"

def download(innerLink):

    print("Iniziato")
    #"C:/Users/samuk/AppData/Roaming/Mozilla/Firefox/Profiles/hciunamq.default-nightly"
    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference("browser.download.manager.showWhenStarting", False)
    profile.set_preference("browser.download.dir", '/tmp')
    profile.set_preference("browser.altClickSave", True)
    #profile.set_preference("browser.helperApps.alwaysAsk.force", False)
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "archive/rar")

    print("Profile set")

    finalDriver = webdriver.Firefox(profile)
    finalDriver.get(innerLink)

    box = finalDriver.find_elements_by_class_name("stream-box")
    print(box[0].text)
    link = box[0].find_elements_by_tag_name("a")[0]
    print(link.get_attribute("href"))

    urllib.request.urlretrieve(link.get_attribute("href"), '/tmp')


    print("clicked")

    finalDriver.close()

def goToDownloadPage(link, nextLink):
    """
        Funzione che scarica il singolo replay
        Apre una nuova finestra del browser e va al link passato come parametro. Poi cerca il link giusto tramite il
        parametro nextLink. Una volta trovato va al link e scarica il replay
    """

    #driver.execute_script(''' window.open( "''' + link +''' ", "_blank").focus();''')
    #print("Aperta")
    #print("Got link")
    #innerResult = driver.find_elements_by_tag_name("a")
    #print(str(len(innerResult)))

    innerDriver = webdriver.Firefox()

    innerDriver.get(link)

    innerResult = innerDriver.find_elements_by_tag_name("a")

    print("Got result")
    for x in innerResult:

        innerLink = x.get_attribute("href")
        #print(innerLink)
        # /matches/2335421/youngsters-vs-heretics-lootbet-season-3
        if type(innerLink).__name__ != "NoneType" and innerLink.find("/matches/") > 0 and nextLink in innerLink:
            if "?" not in innerLink:
                #Dovrei aver ridotto a un solo link. Più test richiesti
                print(innerLink)
                download(innerLink)

    innerDriver.close()


def takePlayerMatches(profileLink):
    """
        Questa funzione prende il link del profilo di un giocatore (che viene passato dal chiamante) e scarica 100
        partite del giocatore di cui gli viene passato il link del profilo.
        Si avvale di un'altra funzione
        è possibile che bisogni specificare i percorsi di Firefox e Chrome anche se non dovrebbe essere necessario
     """

    driver = webdriver.Firefox()

    # driver.maximize_window()
    driver.get(profileLink)

    table = driver.find_elements_by_class_name("stats-table")
    print(str(len(table)))
    resultTd = table[0].find_elements_by_tag_name("td")
    print(resultTd[0].text)

    for counter in range(1):
        # aux conta gli elementi td. Interessano il primo, il secondo e il terzo di ogni riga
        # (i nomi dei team e la data della partita).
        # Ci sono 7 colonne nella tabella
        aux = 7 * counter
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
        print(team)

        enemyTeam = resultTd[aux + 2].text
        # rimozione dei caratteri analoga alla precedente
        enemyTeam = re.sub(" (\([0-9]+\))", "", enemyTeam)
        enemyTeam = enemyTeam.lower()
        print(enemyTeam)

        nextLink = "/" + team + "-vs-" + enemyTeam
        print(nextLink)

        goToDownloadPage(resultA.get_attribute("href"), nextLink)

        print("Scaricato il {} file".format(str(counter + 1) + "°"))

    driver.close()


download("https://www.hltv.org/matches/2335421/youngsters-vs-heretics-lootbet-season-3")
print("Fine")
