from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time 
import datetime
from datetime import date
import pandas as pd
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import numpy as np
import re
from flask import Flask, render_template, request

start_time = time.time()
##################################################### SCRAPING BILLBOARD #####################################################

# Initialise le webdriver avec des options pour améliorer la rapidité
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

# Navigue sur le site Billboard Global 200
driver.get("https://www.billboard.com/charts/billboard-global-200/")

# rejete les cookies
# driver.find_element(By.XPATH,"/html/body/div[6]/div[2]/div/div/div[2]/div/div/button[1]").click()
driver.find_element(By.XPATH,"//*[@id='onetrust-reject-all-handler']").click()

# enleve la box privacy policy
# driver.find_element(By.XPATH,"/html/body/div[5]/div[1]/span").click()

iterateur200 = list(range(1,220,11))
iterateur200.remove(1)

def scraper(list,xpath):
    """
    Permet de scraper chaque élément d'une page trouvé grace à son Xpath. Le texte de cette élement est ensuite ajouté à une liste.\n

    params : 
        list : liste dans laquelle sont stockés tous les éléments trouvés \n
        xpath : le Xpath utilsé pour localisé l'élément (string) \n

    returns : 
        la liste de tous les éléments scrapés sur la page
    """
    for i in range(2,221):
        if i not in iterateur200 : 
            WebElement = driver.find_element(By.XPATH,xpath%(i))
            list.append(WebElement.text)

    return list

def get_dates_of_year_by_week(year, nb_mois):
    """
    Permet d'avoir la date de chaque début de semaine de l'année à partir de la semaine voulue. La date est ensuite ajouté à une liste.\n

    params : 
        year : année concernée (int) \n
        nb_mois : nombre de mois que l'on veut dans l'année en partant de Décembre (int) \n

    returns : 
        la liste de toutes les dates de l'année
    """
    starting_week = 52 - 4 * nb_mois
    current_week = starting_week
    first_day_of_year = datetime.datetime(year, 1, 1)
    week_start = first_day_of_year + datetime.timedelta(days=(current_week - 1) * 7)
    
    while week_start.year == year:
        every_date.append(week_start)
        current_week += 1
        week_start = first_day_of_year + datetime.timedelta(days=(current_week - 1) * 7)
    
    return every_date

def first_day_of_each_week_for_year(year):
    """
    Permet d'avoir la date de chaque début de semaine de l'année. La date est ensuite ajouté à une liste.\n

    params : 
        year : année corcernée (int) \n

    returns : 
        la liste de toutes les dates de l'année
    """
    first_day_of_year = datetime.datetime(year, 1, 1)
    one_week = datetime.timedelta(weeks=1)
    current_week = first_day_of_year
    every_date.append(first_day_of_year)

    while current_week.year == year:
        current_week += one_week
        every_date.append(current_week)

    return every_date

XpathTitle = "/html/body/div[4]/main/div[2]/div[3]/div/div/div/div[2]/div[%d]/ul/li[4]/ul/li[1]/h3"
XpathArtist = "/html/body/div[4]/main/div[2]/div[3]/div/div/div/div[2]/div[%d]/ul/li[4]/ul/li[1]/span"
XpathRank = "/html/body/div[4]/main/div[2]/div[3]/div/div/div/div[2]/div[%d]/ul/li[1]/span "
XpathLastWeek = "/html/body/div[4]/main/div[2]/div[3]/div/div/div/div[2]/div[%d]/ul/li[4]/ul/li[4]/span"
XpathPeakPosition = "/html/body/div[4]/main/div[2]/div[3]/div/div/div/div[2]/div[%d]/ul/li[4]/ul/li[5]/span"
XpathWeeksOnChart = "/html/body/div[4]/main/div[2]/div[3]/div/div/div/div[2]/div[%d]/ul/li[4]/ul/li[6]/span"

allXpath = [XpathTitle,XpathArtist,XpathRank,XpathLastWeek,XpathPeakPosition,XpathWeeksOnChart]

title,artist,rank,last_week,peak_pos,weeks_on_chart = [],[],[],[],[],[]
every_date,list_date = [],[]

allList = [title,artist,rank,last_week,peak_pos,weeks_on_chart]

# on recupère toutes les dates que l'on veut
get_dates_of_year_by_week(2022,3)
first_day_of_each_week_for_year(2023)

for elt_date in every_date:
    elt_date = elt_date.strftime("%Y-%m-%d")
    today = date.today() - datetime.timedelta(weeks=1) # on enlève 1 semaine pour eviter que la semaine actuelle le classement ne soit pas publiée
    if elt_date >= today.strftime("%Y-%m-%d"): # si la date sélectionnée dans la liste est plus grande que la date d'aujourd'hui alors on sort de la boucle
        break
    else : 
        # aller sur la page Billboard de la date correspondante
        driver.get(f"https://www.billboard.com/charts/billboard-global-200/{elt_date}")
        # create a list with the date for all entries (200 per date) 
        [list_date.append(elt_date) for i in range(200)]

        i = [scraper(i,j) for i, j in zip(allList, allXpath)] # scrape les données la page pour tout les Xpaths

df = pd.DataFrame(list(zip(title,artist,rank,last_week,peak_pos,weeks_on_chart,list_date)),columns=['Title','Artist','Rank','Last Week','Peak Position','Weeks on charts','Date'])

# df.to_csv('dataframe.csv',sep=';',index=False)
# print(df)
# Close the webdriver
driver.close()

##################################################### SCRAPING GENIUS #####################################################

# on récupère toutes les chansons (titre,artiste) et l'on enlève toutes les dupplications pour optimiser le temps de scraping
df = pd.read_csv('dataframe.csv',delimiter=';')
df2 = pd.concat([df['Title'],df['Artist']],axis=1)
df2 = df2.drop_duplicates(ignore_index=True)

song_artists = list(zip(df2['Artist'],df2["Title"]))

def format_artiste(char):
    """
    Pour chaque Artiste si il y a une collaboration nous ne prenons que le premier artiste 
    (et donc le principal) pour etre sur d'avoir un résultat dans la recherche Genius. On 
    enlève donc l'artiste en featuring qui suis le caractère par ex With, And, Featuring, &.\n 
    params :
        char : le charctère à partir duquel on tronque la chaine (string)

    returns : 

    """
    for i in range(len(song_artists)):
        if char in song_artists[i][0] and 'Lil Nas X' not in song_artists[i][0]:
            artist_list = list(song_artists[i])
            artist_list[0] = artist_list[0][:artist_list[0].index(char)]
            song_artists[i] = tuple(artist_list)


format_artiste(" vs. ")
format_artiste(" With ")
format_artiste(" X ")
format_artiste(" x ")
format_artiste(" & ")
format_artiste(" Featuring ")
format_artiste(" And ")
format_artiste(" E ")

for i in [380,474,519]:
    song_artists.pop(i)
    df2 = df2.drop(i)

# initialisation du driver_genius avec des options
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
driver_genius = webdriver.Chrome(ChromeDriverManager().install(), options=options)

# ouvrir le site et accepter les cookies

driver_genius.get("https://genius.com/")

driver_genius.implicitly_wait(3)
driver_genius.find_element(By.ID,"onetrust-accept-btn-handler").click()

 
song,artist,date_sortie,producteurs_text,ecrivains_text,publisher_text,distributor_text,Tags = [],[],[],[],[],[],[],[]


for i in range(len(song_artists)):

    driver_genius.get("https://genius.com/")

    # activer la recherche
    element = driver_genius.find_element(By.XPATH,"/html/body/div[1]/div/div[1]/div[1]/form/input")
    element.send_keys(song_artists[i][1]+' '+song_artists[i][0], Keys.ENTER)

    song.append(song_artists[i][1])
    artist.append(song_artists[i][0])
    # driver_genius.implicitly_wait(3)

    # clicker sur la chanson
    try :
        
        driver_genius.implicitly_wait(3)
        driver_genius.find_element(By.XPATH,"/html/body/routable-page/ng-outlet/search-results-page/div/div[2]/div[1]/div[1]/search-result-section/div/div[2]/search-result-items/div/search-result-item/div/mini-song-card/a/div[2]").click()
        # driver_genius.implicitly_wait(3)
    
    except:

        driver_genius.implicitly_wait(3)
        driver_genius.find_element(By.XPATH,"/html/body/routable-page/ng-outlet/search-results-page/div/div[2]/div[1]/div[2]/search-result-section/div/div[2]/search-result-items/div[1]/search-result-item/div/mini-song-card/a").click()
        # driver_genius.implicitly_wait(3)


    # scroll to credits

    target_credits = driver_genius.find_element(By.CSS_SELECTOR,"div.SongInfo__Title-nekw6x-1")
    driver_genius.execute_script("arguments[0].scrollIntoView();", target_credits)

    # Si le bouton expand est présent

    try: 
        #click on expand if this button exist

        all_elements_after_target_credit = target_credits.find_elements(By.XPATH, ".//following::*")

        # trouve le 1er element dont le tag_name est "button"

        for element in all_elements_after_target_credit:
            if element.tag_name == "button" and "Expand" in element.text:
                element.click()
                break
    
    except:

        # Le bouton Expand n'a pas été trouvé sur la page
        print("Le bouton n'existe pas sur la page")

    ############################################## DATE ####################################################   
    try:

        # Localiser la balise "div" contenant la date en utilisant son contenu texte
        date_element = driver_genius.find_element(By.XPATH,"//div[contains(text(),'Release Date')]")

        # Extraire la date à partir du texte en utilisant des expressions régulières
        if date_element:
            date_text = date_element.find_element(By.XPATH,'./following-sibling::div').text
            date_regex = r"\w+\s+\d{1,2},\s+\d{4}"
            time.sleep(2)
            match = re.search(date_regex, date_text)
            if match:

                date_sortie.append(match.group())
        
        # driver_genius.implicitly_wait(10)

    except:

        date_sortie.append("None")

    # Recherche des producteurs, ecrivains, publisher, distributor et tags

    ################################################## PRODUCTEURS #############################################
    try:
        producteurs_element = driver_genius.find_element(By.XPATH,"//div[contains(text(),'Produced By')]")
        producteurs_text.append(producteurs_element.find_element(By.XPATH,'./following-sibling::div').text)
    except:
        producteurs_text.append("None")
    ############################################ ECRIVAIN ######################################################
    try:
        ecrivains_element = driver_genius.find_element(By.XPATH,"//div[contains(text(),'Written By')]")
        ecrivains_text.append(ecrivains_element.find_element(By.XPATH,'./following-sibling::div').text)
    except:  
        ecrivains_text.append("None")

    ####################################### DISTIBUTEURS #######################################################
    try:
        distributor_element = driver_genius.find_element(By.XPATH,"//div[contains(text(),'Distributor')]")
        distributor_text.append(distributor_element.find_element(By.XPATH,'./following-sibling::div').text)
    except:
        distributor_text.append("None")

    ############################################ TAGS ##########################################################

    try:
        tag_pos = driver_genius.find_element(By.CLASS_NAME,"SongTags__Title-xixwg3-0")
        driver_genius.execute_script("arguments[0].scrollIntoView();", tag_pos)
        name = driver_genius.find_elements(By.CLASS_NAME, "SongTags__Container-xixwg3-1")

        tag=[]

        for elt in name:

            tag.append(elt.text)

        tags = ''.join(set(tag))  
        
        Tags.append(tags.replace('\n',', '))


    except:

        Tags.append("None")
    
        driver_genius.get("https://genius.com/") # on revient à l'accueil

    print(i,song_artists[i][1]+' '+song_artists[i][0])

driver_genius.close()

list_title = list(df2['Title'])
list_artist = list(df2['Artist'])
df_genius_557 = pd.DataFrame({'Title':list_title, 'Artist':list_artist,'Genre':Tags,'Producers':producteurs_text,'Writers':ecrivains_text,'Distributor':distributor_text})

# df_genius_557.to_csv('data_sans_doublons.csv_test',sep=';', index=False)

print(df_genius_557.info())

# df = pd.read_csv('dataframe.csv',delimiter=';')
list_genre, list_writers, list_producers, list_distributor  = [],[],[],[]

# Cette boucle permet de parcourir la df initiale avec toutes les pages scrapées sur le site Billboard (4200 lignes).
# On la compare ensuite à df_genius_557 qui contient tout le reste des informations récupérées sur Genius pour toutes les chansons sans doublons (557 lignes).
# Si un match est trouvé avec le couple (artiste, titre) on ajoute à la ligne correspondante de la df intiale le reste des informations trouvées sur Genius
# Cela permet un gain de temps pour le scraping Genius qui ai déja très long (un scraping sur 557 chansons et non 4200)

for value in df.iterrows():
    title1 = value[1][0]
    artist1 = value[1][1]
    # print(value[0])
    match_found = False
    for value2 in df_genius_557.iterrows():
        title2 = value2[1][0]
        artist2 = value2[1][1]

        if artist1 == artist2 and title1==title2:
            list_genre.append(value2[1][2])
            list_producers.append(value2[1][3])
            list_writers.append(value2[1][4])         
            list_distributor.append(value2[1][5])
            match_found = True
            break
    if not match_found:
        list_genre.append("Null")
        list_writers.append("Null")
        list_producers.append("Null")
        list_distributor.append("Null")
    
df_inter = pd.DataFrame({'Genre':list_genre,'Producers':list_producers,'Writers':list_writers,'Distributor':list_distributor})

df_finale = pd.concat([df, df_inter], axis=1)

# df_finale.to_csv('dataframe_finale_test.csv',sep=';', index=False)
print(df_finale.info())
##################################################### ELASTIC SEARCH #####################################################

df_finale = pd.read_csv('dataframe_finale.csv',delimiter=';')
# conversion des variables et formatage
df_finale['Last Week'] = df_finale['Last Week'].replace("-",0)
df_finale['Last Week']= df_finale['Last Week'].astype('int64')
df_finale['Date'] = pd.to_datetime(df_finale['Date'])

data = df_finale.to_dict('records')

# séparation des strings dans plusieurs catégories
for i,song in enumerate(data):
    song['Genre'] = re.split(', | & ', song['Genre'])
    song['Producers'] = re.split(', | & ', song['Producers'])
    try:
        song['Writers'] = re.split(', | & ', song['Writers'])
    except TypeError:
        data[i]["Writers"] = "None"
        song['Writers'] = re.split(', | & ', song['Writers'])
    try:
        song['Distributor'] = re.split(', | & ', song['Distributor'])
    except TypeError:
        data[i]["Distributor"] = "None"
        song['Distributor'] = re.split(', | & ', song['Distributor'])

# démarrage ElasticSearch
es = Elasticsearch([{'host': 'localhost', 'port': 9200,"scheme": "http"}])

# indexation des données dans elastic search
def generate_data(data):
    for docu in data:
        yield {
            "_index": "billboard",
            "_type": "song",
            "_source": {k:v if v else None for k,v in docu.items()},
        }
        
if es.indices.exists('billboard')==True:
    es.indices.delete(index='billboard')
    bulk(es, generate_data(data))
else :
    bulk(es, generate_data(data))


##################################################### FLASK APP ##########################################################
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form['query']
        # field = request.form['field']
        field = request.form.get('field')
        results = search(query, field)
        return render_template('index.html', results=results)
    else:
        return render_template('index.html')

def search(query, field):
    QUERY ={
    "query": {
        "bool": {
        "must": [],
        "filter": [
            {
            "bool": {
                "should": [
                {
                    "match_phrase": {
                    field : query
                    }
                }
                ],
                "minimum_should_match": 1
            }
            }
        ],
        "should": [],
        "must_not": []
        }
    }
    }
    result = es.search(index="billboard", body=QUERY,size=4200)

    results = []
    [results.append(elt['_source']) for elt in result["hits"]["hits"]]

    return results

if __name__ == '__main__':
    app.run(debug=True)


# Lancer la page (pour l'instant) avec la commande "flask --app scraper_test run"

end_time = time.time()
execution_time = end_time - start_time

print("Temps d'exécution : ", execution_time, " secondes")