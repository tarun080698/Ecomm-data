import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
# Regex pattern to match the code
pattern = r'\b(?:AA|E|B)\d{1,4}\b'
# The URL of the main listing page
listing_url_base = 'https://www.newyorkcitytop.shop/brand/Milano%20Formals/page/'


# Function to get the list of product URLs and their corresponding codes from the local HTML file
def get_product_info_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    soup = BeautifulSoup(content, 'html.parser')

    # Find all product links and titles
    product_cards = soup.select('.product')

    product_info = []

    for card in product_cards:
        # Extract the product URL
        product_link = card.select_one('.thumbimage div a')
        product_url = product_link['href'] if product_link else None
        title = card.select_one(".thumbname")
        title = title.text.strip() if title else ""
        match = re.search(pattern, title)

        code = None
        if match:
            code = match.group(0)

        product_info.append({'url': product_url, 'code': code})

    return product_info


# Function to get the list of product URLs and their corresponding codes from the listing page


def get_product_info(listing_url):
    response = requests.get(listing_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all product links and titles
    product_cards = soup.select('.product')

    print(product_cards[0])
    product_info = []

    for card in product_cards:
        # Extract the product URL
        product_link = card.select_one('.thumbimage div a')
        product_url = product_link['href']
        title = card.select_one(".thumbname")
        title = title.text.strip()
        match = re.search(pattern, title)

        code = None
        if match:
            code = match.group(0)
            print("Extracted Code:", code)

        # og_title = product_url.split("/")[1]

        # # Extract the product title to get the code
        # # title = og_title.text.strip()
        # # Assuming the code is the third word in the title
        # code = og_title.split("-")[2]

        product_info.append({'url': product_url, 'code': code})

    return product_info

# Function to scrape the description from a product page


def get_product_description(product_url):
    response = requests.get(product_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract the product description
    # Adjust the selector as necessary
    # description = soup.select_one('div#description').text.strip()
    description_div = soup.find('div', id='description')
    description = description_div.text.strip(
    ) if description_div else "No description found."

    return description


data = []
# Get the product info including URLs and codes
# for i in range(1, 14):
products = get_product_info_from_file("data/extras/index.html")

for product in products:
    print(product['code'])
    # Ensure the product URL is complete
    full_url = f'https://www.lookmazing.com{product["url"]}'
    description = get_product_description(full_url)
    data.append({
        'Code': product['code'],
        'Description': description,
        'URL': full_url
    })

# Save the data to a CSV file


df = pd.DataFrame(data)
df.to_csv('product_descriptions_with_codes.csv', index=False, mode="a",)

print("Product descriptions and codes have been saved to 'product_descriptions_with_codes.csv'.")
