import requests

url = "https://www.billboard.com/charts/billboard-global-200/"
response = requests.get(url)
response.status_code