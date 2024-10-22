from re import L
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urljoin
from urllib.request import urlretrieve
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from fake_useragent import UserAgent
import requests
import time
import json


products = []


def setup_driver():
    # Set up the Selenium Chrome driver
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-extensions")
    # Remove this line if you want to see the browser.
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    return driver


def download_images(images, save_path):
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    for idx, product in enumerate(images):
        filename = product['filename']

        image_url = product['image_url']
        try:
            # Generate a random user agent
            request = Request(image_url, headers={
                              'User-Agent': UserAgent().random})
            response = urlopen(request).read()

            # Save the image
            filepath = os.path.join(save_path, filename)
            with open(filepath, 'wb') as f:
                f.write(response)
        except Exception as e:
            break


def download_images_additional(images, save_path):
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    for idx, product in enumerate(images):

        # image_url = product['image_url']
        for idy, img in enumerate(product['additional_images_url']):
            name_part, extension = product['filename'].rsplit('.', 1)

            filename = f"{name_part}_{idy+1}.{extension}"
            try:
                # Generate a random user agent
                request = Request(img, headers={
                    'User-Agent': UserAgent().random})
                response = urlopen(request).read()

                # Save the image
                filepath = os.path.join(save_path, filename)
                with open(filepath, 'wb') as f:
                    f.write(response)
            except Exception as e:
                break


def fetch_images_from_overlay(index, driver, save_path):
    # Click the main image to open the overlay
    main_image = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "mainImgA")))
    main_image.click()

    # Wait for the overlay to appear
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "fancybox-overlay")))

    while True:
        # Get the current image URL
        image_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "fancybox-image")))
        image_src = image_element.get_attribute('src')

        if 'additional_images_url' in products[index] and image_src in products[index]['additional_images_url']:
            break
        if 'additional_images_url' in products[index]:
            products[index]['additional_images_url'].append(image_src)
        else:
            products[index]['additional_images_url'] = [image_src]

        # Try to click the 'next' button, if fails, break the loop
        try:
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "fancybox-next")))
            next_button.click()
            time.sleep(1)  # Small delay to allow the next image to load
        except Exception as e:
            break


def get_description(url,idx):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        soup = BeautifulSoup(response.text, 'html.parser')
        description_div = soup.find(id='tab-description')
        if description_div:
            products[idx]['description'] = description_div.get_text(strip=True)
        else:
            return ""
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return ""

def go_inside_product(url, index, type):
    save_path = "downloaded_images"

    driver = setup_driver()
    driver.get(url)

    try:
        if type=="info":
            get_description(url,index)
        else:
            fetch_images_from_overlay(index, driver, save_path)
    finally:
        driver.quit()


def extract_image_details(soup, base_url):
    # products = []  # List to hold product dictionaries
    for product in soup.find_all("div", class_="product-block"):
        image_tag = product.find("img")
        link_tag = product.find("a", class_="img")
        price_div = product.find('span', class_="money")
        product_info = {}
        if image_tag:
            alt_text = image_tag.get("alt", "")
            product_details = alt_text.split()
            product_code = product_details[-1]
            product_name = " ".join(product_details[0:-1])
            filename = f"{product_code}_{product_name}.jpg".replace(
                " ", "_").replace("/", "_")

            # Populate the dictionary with product details
            product_info['name'] = product_name
            product_info['code'] = product_code
            # product_info['image_url'] = image_url
            product_info['filename'] = filename

        if link_tag and 'href' in link_tag.attrs:
            detail_url = urljoin(base_url, link_tag['href'])
            product_info['detail_url'] = detail_url

        if price_div:
            product_info['price'] = price_div.get_text(strip=True)
        # Append the product dictionary to the list if it contains essential information
        if product_info:
            products.append(product_info)

    return products


def parse_html(html):
    return BeautifulSoup(html, 'html.parser')


def fetch_html(url):
    try:
        headers = {'User-Agent': UserAgent().random}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching the webpage: {e}")
        return None


def main():
    url = "https://www.bellasposabridalandprom.com/c83123/milano-formals.html"
    html = fetch_html(url)
    if html:
        soup = parse_html(html)
        extract_image_details(soup, url)
        # download_images(products, save_path)

        for idx, product in enumerate(products):
            go_inside_product(product['detail_url'], idx, type='info')

        with open('products.json', 'a') as json_file:
            json.dump(products, json_file, indent=4)

    # with open('glitterati_products.json', 'r') as json_file:
    #     data = json.load(json_file)

    # download_images_additional(data, save_path)


if __name__ == "__main__":
    main()
