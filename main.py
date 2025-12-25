import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd

seen_urls = set()           # Track what we've already processed
company_data = []           # Store all scraped data

url = "https://www.futuretools.io/"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
companies = soup.find_all("div", class_="div-block-59")
for company in companies:
    # Check if we've already seen this URL
    link = urljoin(url, company.find("a", class_="tool-item-link---new")["href"])
    if link in seen_urls:
        continue
    seen_urls.add(link)
    # Extract basic information
    name = company.find("a", class_="tool-item-link---new").text
    description = company.find("div", class_="tool-item-description-box---new").text
    category = company.find("div", class_="text-block-53").text
    upvotes = int(company.find(
        "div", class_="text-block-52 jetboost-item-total-favorites-vd2l"
    ).text)

    # Navigate detailed page
    company_response = requests.get(link)
    company_soup = BeautifulSoup(company_response.text, 'html.parser')

    # Extract additional information
    company_link = company_soup.select_one(
        "div.div-block-6.vertical-flex a"
    )['href']
    price = company_soup.select_one("div.div-block-17 div.text-block-2").text

    company_data.append({
        "Name": name,
        "Category": category,
        "Price": price,
        "Upvotes": upvotes,
        "Description": description,
        "Link": company_link
    })



