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
driver.get("https://www.billboard.com/charts/hot-100/")

# Wait for the page to load
driver.implicitly_wait(10)

iterateur = list(range(1,110,11))
iterateur.remove(1)

def scraper(list,xpath):
    for i in range(2,111):
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

title = scraper(title,XpathTitle)
artist = scraper(artist,XpathArtist)
rank = scraper(rank,XpathRank)
last_week = scraper(last_week,XpathLastWeek)
peak_pos = scraper(peak_pos,XpathPeakPosition)
weeks_on_chart = scraper(weeks_on_chart,XpathWeeksOnChart)

df = pd.DataFrame(list(zip(title,artist,rank,last_week,peak_pos,weeks_on_chart)),columns=['Title','Artist','Rank','Last Week','Peak Positon','Weeks on charts'])
print(df)

# Close the webdriver
driver.close()

end = time.time()
temps = end - start
print("temps d'execution :",temps,"s")