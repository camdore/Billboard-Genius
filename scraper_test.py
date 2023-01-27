from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import time 
import pandas as pd

start = time.time()
# Initialize the webdriver
# de manière basique
# driver = webdriver.Chrome()

# avec ChromeDriverManager mieux car update du driver automatiquement
driver = webdriver.Chrome(ChromeDriverManager().install())

# si on a télécharger le driver directement dans le dossier 
# service = Service(executable_path="./chromedriver.exe")
# driver = webdriver.Chrome(service=service)

# Navigate to the website
# driver.get("https://www.billboard.com/charts/hot-100/")
# driver.get("https://www.billboard.com/charts/billboard-global-200/")
driver.get("https://www.billboard.com/charts/billboard-200/")

# Wait for the page to load
driver.implicitly_wait(10)

iterateur100 = list(range(1,110,11))
iterateur100.remove(1)
iterateur200 = list(range(1,220,11))
iterateur200.remove(1)

# 111 ou 221

def scraper(list,xpath,iterateur,nb_max):
    for i in range(2,nb_max):
        if i not in iterateur : 
            WebElement = driver.find_element(By.XPATH,xpath%(i))
            list.append(WebElement.text)

    return list

XpathTitle = "/html/body/div[4]/main/div[2]/div[3]/div/div/div/div[2]/div[%d]/ul/li[4]/ul/li[1]/h3"
XpathArtist = "/html/body/div[4]/main/div[2]/div[3]/div/div/div/div[2]/div[%d]/ul/li[4]/ul/li[1]/span"
XpathRank = "/html/body/div[4]/main/div[2]/div[3]/div/div/div/div[2]/div[%d]/ul/li[1]/span "
XpathLastWeek = "/html/body/div[4]/main/div[2]/div[3]/div/div/div/div[2]/div[%d]/ul/li[4]/ul/li[4]/span"
XpathPeakPosition = "/html/body/div[4]/main/div[2]/div[3]/div/div/div/div[2]/div[%d]/ul/li[4]/ul/li[5]/span"
XpathWeeksOnChart = "/html/body/div[4]/main/div[2]/div[3]/div/div/div/div[2]/div[%d]/ul/li[4]/ul/li[6]/span"

title = []
artist = []
rank = []
last_week =[]
peak_pos = []
weeks_on_chart = []

title = scraper(title,XpathTitle,iterateur200,221)
artist = scraper(artist,XpathArtist,iterateur200,221)
rank = scraper(rank,XpathRank,iterateur200,221)
last_week = scraper(last_week,XpathLastWeek,iterateur200,221)
peak_pos = scraper(peak_pos,XpathPeakPosition,iterateur200,221)
weeks_on_chart = scraper(weeks_on_chart,XpathWeeksOnChart,iterateur200,221)

df = pd.DataFrame(list(zip(title,artist,rank,last_week,peak_pos,weeks_on_chart)),columns=['Title','Artist','Rank','Last Week','Peak Positon','Weeks on charts'])
print(df)

# Close the webdriver
driver.close()

end = time.time()
temps = end - start
print("temps d'execution :",temps,"s")