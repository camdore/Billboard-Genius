from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import time 

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

def cleanlist(webElements,alist):
    for i in range(len(webElements)):
        if len(webElements[i].text)!= 0:
            alist.append(webElements[i].text)

    return alist 

# Extract the song title and artist
titres = driver.find_elements(By.CLASS_NAME,"c-title")
ltitres = []
ltitres = cleanlist(titres,ltitres)

# on elève tout les index en trop
ltitres.pop(1)  
for i in range(100,len(ltitres)):
    ltitres.pop()

# print(ltitres)
# print(len(ltitres))

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