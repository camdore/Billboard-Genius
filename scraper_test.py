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
from pymongo import MongoClient

start = time.time()
# Initialize the webdriver
# avec ChromeDriverManager mieux car update du driver automatiquement
driver = webdriver.Chrome(ChromeDriverManager().install())

# Navigate to the website
# driver.get("https://www.billboard.com/charts/hot-100/")
driver.get("https://www.billboard.com/charts/billboard-global-200/")
# driver.get("https://www.billboard.com/charts/billboard-200/")

# Wait for the page to load
# driver.implicitly_wait(10)
time.sleep(50)

# reject all cookies
driver.find_element(By.XPATH,"/html/body/div[6]/div[2]/div/div/div[2]/div/div/button[1]").click()

# enlever la box privacy policy
driver.find_element(By.XPATH,"/html/body/div[5]/div[1]/span").click()

iterateur100 = list(range(1,110,11))
iterateur100.remove(1)
iterateur200 = list(range(1,220,11))
iterateur200.remove(1)

# nb_max 111 ou 221
def scraper(list,xpath,iterateur,nb_max):
    for i in range(2,nb_max):
        if i not in iterateur : 
            WebElement = driver.find_element(By.XPATH,xpath%(i))
            list.append(WebElement.text)

    return list

def get_dates_of_year_by_week(year, nb_mois):
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
get_dates_of_year_by_week(2022,2)
first_day_of_each_week_for_year(2023)

for elt_date in every_date:
    elt_date = elt_date.strftime("%Y-%m-%d")
    today = date.today() - datetime.timedelta(weeks=1) # on enlève 1 semaine pour eviter que la semaine actuelle le classement ne soit pas publié
    if elt_date >= today.strftime("%Y-%m-%d"): # si la date sélectionnée dans la liste est plus grande que la date d'aujourd'hui alors on sort de la boucle
        break
    else : 
        # get on the correct billboard page 
        driver.get(f"https://www.billboard.com/charts/billboard-global-200/{elt_date}")
        # create a list with the date for all entries (200 per date) 
        [list_date.append(elt_date) for i in range(200)]
        # scrape all the data
        i = [scraper(i,j,iterateur200,221) for i, j in zip(allList, allXpath)]

df = pd.DataFrame(list(zip(title,artist,rank,last_week,peak_pos,weeks_on_chart,list_date)),columns=['Title','Artist','Rank','Last Week','Peak Positon','Weeks on charts','Date'])
print(df)
df.to_csv('dataframe.csv',index=False)
# Close the webdriver
driver.close()

genius =  list(zip(title, artist))

# partie MongoDB
data = df.to_dict('records')
# data = df.to_json('records')

# Connect to the MongoDB database
client = MongoClient("mongodb://localhost:27017/")
db = client["mydatabase"]
collection = db["mycollection"]

# insérer le json/dict dans la db
collection.insert_many(data)
collection.find_one()
cursor = collection.find()
# for document in cursor :
#     print('-----')
#     print(document)


end = time.time()
temps = end - start
print("temps d'execution :",temps,"s")

print(df['Title']['Black Panther: Wakanda Forever (Music from and Inspired By)'])


# for i in song_artists[0:3]:

#     driver.get('https://genius.com/{}-lyrics'.format(str(i[0]))) #ensemble des sites internet
#     # driver.find_element(By.XPATH,"/html/body/div[7]/div[3]/div[1]/div/div[2]/div/button[1]").click()
# driver.quit()

# Les Xpaths des cookies changent:

#/html/body/div[1]/main/div[1]/div[3]/div[1]/div[2]/div/div[1]/span[1]/span sos sza
#/html/body/div[1]/main/div[1]/div[4]/div/div[1]/div[2]/div
