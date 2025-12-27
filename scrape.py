import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
import time
import os

seen_urls = set()  # Track what we've already processed
company_data = []  # Store all scraped data


# Load existing data to global variables
def load_existing_data():
    global seen_urls, company_data

    if os.path.exists("ai_data.csv"):
        df = pd.read_csv("ai_data.csv")
        company_data = df.to_dict("records")
        seen_urls = set(item["Link"] for item in company_data)
        print(f"Loaded {len(seen_urls)} existing entries.")


def scrape_all_pages():
    global seen_urls, company_data

    base_url = "https://www.futuretools.io/"
    page = 1

    while True:
        # Construct the URL for the current page
        # Page 1 uses base URL, pages 2+ use the parameter
        if page == 1:
            url = base_url
        else:
            url = f"{base_url}?b34cbd71_page={page}"
        print(f"Scraping page: {page}")

        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        new_items = 0  # Track new items found on this page
        try:
            # Find all companies in the current page
            companies = soup.find_all("div", class_="div-block-59")

            # If no companies found, we've reached the last page
            if not companies:
                print(f"No companies found on page {page}. Stopping.")
                break

            # Process each company
            for company in companies:
                # Check if we've already seen this URL
                link_element = company.find("a", class_="tool-item-link---new")
                if not link_element:
                    continue
                link = urljoin(url, link_element["href"])
                if link in seen_urls:
                    continue
                seen_urls.add(link)
                new_items += 1

                # Extract basic information
                name = link_element.text
                description = company.find(
                    "div", class_="tool-item-description-box---new"
                ).text
                category = company.find("div", class_="text-block-53").text
                upvotes = int(
                    company.find(
                        "div", class_="text-block-52 jetboost-item-total-favorites-vd2l"
                    ).text
                )

                # Navigate detailed page
                try:
                    company_response = requests.get(link)
                    company_soup = BeautifulSoup(company_response.text, "html.parser")

                    # Extract additional information
                    company_link = company_soup.select_one(
                        "div.div-block-6.vertical-flex a"
                    )["href"]
                    price = company_soup.select_one(
                        "div.div-block-17 div.text-block-2"
                    ).text

                    company_data.append(
                        {
                            "Name": name,
                            "Category": category,
                            "Price": price,
                            "Upvotes": upvotes,
                            "Description": description,
                            "Link": company_link,
                        }
                    )
                    time.sleep(0.5)
                except Exception as e:
                    print(f"Error scraping {link}: {e}")

            if new_items == 0:
                print(f"No new items found on page {page}")
            else:
                print(f"Found {new_items} new items on page {page}")
            page += 1  # Move to the next page
            time.sleep(1)

        except Exception as e:
            print(f"Error processing page {page}: {e}")
            break


# load_existing_data()
# scrape_all_pages()