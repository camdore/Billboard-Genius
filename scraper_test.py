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

artistes = driver.find_elements(By.CLASS_NAME,"c-label")
lartistes = []
lartistes = cleanlist(artistes,lartistes)

# on enlève tout les index en trop bis
del lartistes[0:3]
for value in lartistes:
    if value == 'NEW' or value == 'RE- ENTRY':
        lartistes.remove(value) 

# print(lartistes)
print(len(lartistes))

classement = []
for value in lartistes:
    if value == '-' or value.isnumeric()== True:
        classement.append(value)

for index,value in enumerate(lartistes):
    if value == '-' or value.isnumeric() == True:
        lartistes.pop(index)

# print(lartistes)
print(len(lartistes))
# print(classement)
# print(len(classement))

# Close the webdriver
driver.close()

end = time.time()
temps = end - start
print("temps d'execution :",temps,"s")