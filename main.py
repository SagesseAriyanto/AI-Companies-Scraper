import requests
from bs4 import BeautifulSoup

url = "https://www.futuretools.io/"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
companies = soup.find_all("div", class_="div-block-59")
for company in companies:
    print(company.text.strip())