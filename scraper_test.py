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
# driver.implicitly_wait(10)
time.sleep(50)

# reject all cookies
driver.find_element(By.XPATH,"/html/body/div[6]/div[2]/div/div/div[2]/div/div/button[1]").click()

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

XpathTitle = "/html/body/div[4]/main/div[2]/div[3]/div/div/div/div[2]/div[%d]/ul/li[4]/ul/li[1]/h3"
XpathArtist = "/html/body/div[4]/main/div[2]/div[3]/div/div/div/div[2]/div[%d]/ul/li[4]/ul/li[1]/span"
XpathRank = "/html/body/div[4]/main/div[2]/div[3]/div/div/div/div[2]/div[%d]/ul/li[1]/span "
XpathLastWeek = "/html/body/div[4]/main/div[2]/div[3]/div/div/div/div[2]/div[%d]/ul/li[4]/ul/li[4]/span"
XpathPeakPosition = "/html/body/div[4]/main/div[2]/div[3]/div/div/div/div[2]/div[%d]/ul/li[4]/ul/li[5]/span"
XpathWeeksOnChart = "/html/body/div[4]/main/div[2]/div[3]/div/div/div/div[2]/div[%d]/ul/li[4]/ul/li[6]/span"

allXpath = [XpathTitle,XpathArtist,XpathRank,XpathLastWeek,XpathPeakPosition,XpathWeeksOnChart]

title,artist,rank,last_week,peak_pos,weeks_on_chart = [],[],[],[],[],[]

allList = [title,artist,rank,last_week,peak_pos,weeks_on_chart]

i = [scraper(i,j,iterateur200,221) for i, j in zip(allList, allXpath)]

# for i, j in zip(allList, allXpath):
#     i = scraper(i,j,iterateur200,221)

df = pd.DataFrame(list(zip(title,artist,rank,last_week,peak_pos,weeks_on_chart)),columns=['Title','Artist','Rank','Last Week','Peak Positon','Weeks on charts'])
print(df)

# Close the webdriver
driver.close()

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
