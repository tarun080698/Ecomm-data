import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from urllib.parse import urljoin


def scrape_product_details(name, link):
    # Send a GET request to the webpage
    response = requests.get(link)
    response.raise_for_status()  # Check if the request was successful

    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all product blocks
    product_blocks = soup.find_all('div', class_='product-block item-default')
    # Collect the data
    data = []
    for product in product_blocks:
        # Extract the product name
        name_tag = product.find('h3', class_='name').find('span')
        product_name = name_tag.text if name_tag else None

        if "milano" in product_name.lower():
            product_code = product_name.split(" ")[0]
            # Extract the product link
            link_tag = product.find('a', class_='img')
            product_link = urljoin(link, link_tag.get(
                'href')) if link_tag else None

            # Extract the product price
            price_tag = product.find('div', class_='price').find(
                'span', class_='money')
            product_price = price_tag.text.strip() if price_tag else None

            # Append the data
            data.append([name, product_link, product_code,
                        product_name, product_price])

    return data


def save_to_csv(data, filename):
    # Check if file exists to determine the header
    file_exists = os.path.exists(filename)

    # Create a DataFrame
    df = pd.DataFrame(data, columns=[
                      'Source Page', 'Product URL', 'Product Code', 'Product Name', 'Product Price'])

    # Append the DataFrame to a CSV file
    df.to_csv(filename, mode='a', header=not file_exists, index=False)


def main():
    urls = [
        {"name": "bellasposabridalandprom.com",
            "link": 'https://www.bellasposabridalandprom.com/sub.php?sStyle=milano+formals&Page=Search'},
        {"name": "bellasposabridalandprom.com",
            "link": 'https://www.bellasposabridalandprom.com/sub.php?thisOffset=96&CatId=&sStyle=milano%20formals&sType=sStyle&Page=Search&'},
        {"name": "vipfashionbridals.com",
            "link": 'https://www.vipfashionbridals.com/sub.php?sStyle=milano+formals&Page=Search'},
        {"name": "bridalprompageant.com",
            "link": 'https://www.bridalprompageant.com/sub.php?sStyle=milano&Page=Search', },
        {"name": "bridalprompageant.com",
            "link": 'https://www.bridalprompageant.com/c74262/milano-formals-shorts.html', },
        {"name": "glitteratistyle.com",
            "link": 'https://www.bellasposabridalandprom.com/sub.php?sStyle=milano+formals&Page=Search', },
        {"name": "glitteratistyle.com",
            "link": 'https://www.glitteratistyle.com/sub.php?thisOffset=96&CatId=&sStyle=milano&sType=sStyle&Page=Search&', }
    ]

    # Filename of the CSV file
    filename = 'products.csv'

    # Scrape and save data for each URL
    for url in urls:
        name, link = url['name'], url['link']
        data = scrape_product_details(name, link)
        if data:
            save_to_csv(data, filename)
            print(f"Data from {name} saved to {filename}")
        else:
            print(f"No data to save from {name}.")


if __name__ == '__main__':
    main()
