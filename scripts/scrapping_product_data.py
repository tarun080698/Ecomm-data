import json
import requests
from bs4 import BeautifulSoup

# Function to get the description from a webpage


def get_description(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        soup = BeautifulSoup(response.text, 'html.parser')
        description_div = soup.find(id='tab-description')
        if description_div:
            return description_div.get_text(strip=True)
        else:
            return ""
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return ""


# Load the JSON file
with open('our_products.json', 'r') as json_file:
    data = json.load(json_file)

# Iterate over the list of dicts and update with description
for item in data:
    url = item.get('detail_url')
    if url:
        description = get_description(url)
        item['description'] = description

# Save the updated list of dicts to a new JSON file
with open('our_products_new.json', 'w') as output_file:
    json.dump(data, output_file, indent=4)

print('Updated data has been written to output.json')
