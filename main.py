import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

url = "https://www.futuretools.io/"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
companies = soup.find_all("div", class_="div-block-59")
for company in companies:
    name = company.find("a", class_="tool-item-link---new").text
    description = company.find("div", class_="tool-item-description-box---new").text
    market = company.find("div", class_="text-block-53").text
    link =  urljoin(url, company.find("a", class_="tool-item-link---new")["href"])
    upvotes = int(company.find(
        "div", class_="text-block-52 jetboost-item-total-favorites-vd2l"
    ).text)
    print(f"Name: {name}\nDescription: {description}\nMarket: {market}\nLink: {link}\nUpvotes: {upvotes}\n")
