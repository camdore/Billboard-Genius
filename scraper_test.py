from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

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

# Extract the song title and artist
titres = driver.find_elements(By.CLASS_NAME,"c-title")
# for i in range(50):
#     print(titres[i].text)

artistes = driver.find_elements(By.CLASS_NAME,"c-label")
# for i in range(50):
#     print(artistes[i].text)
print(type(artistes[1].text))
# print(len(artistes),len(titres))

# Close the webdriver
driver.close()