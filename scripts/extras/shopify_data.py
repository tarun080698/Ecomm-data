import json
import csv

# Define the required headers for the new CSV
headers = ["Handle", "Title", "Body (HTML)", "Description", "Vendor", "Type", "Product Category", "Tags", "Location", "Option1 Name", "Option1 Value", "Option2 Name", "Option2 Value", "Image Src", "Variant SKU",
           "Variant Inventory Qty", "Variant Price", "Variant Inventory Policy", "Variant Requires Shipping", "Variant Taxable", "Variant Inventory Tracker"
           #    , "SKU", "HS Code", "COO", "Incoming", "Unavailable", "Committed", "Available", "On hand"
           ]

# Load the JSON file
with open('all_products.json', 'r') as json_file:
    json_data = json.load(json_file)

# Open a new CSV file for writing
with open('csv_data/all_shopify_data.csv', 'w', newline='') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=headers)

    # Write the header row
    writer.writeheader()

    # Write the JSON data to the CSV file
    for index, item in enumerate(json_data):
        img = item["additional_images_url"][0]
        # Create a dictionary for the CSV row
        if "variants" in item.keys():
            for variant in item['variants']:
                # location = str(variant['location'])
                csv_row = {
                    "Handle": item.get("code").lower(), #product_code
                    "Title": item.get("code") + " " + item.get("name"), #gpt
                    "Body (HTML)": item.get("description"), #gpt
                    "Vendor": "Milano Formals",
                    "Type": "Dress",
                    "Product Category": "Apparel & Accessories > Clothing > Dresses",
                    "Option1 Name": "Size",
                    "Option1 Value": variant['size'],
                    "Option2 Name": "Color",
                    "Option2 Value": variant['color'],
                    "Image Src": img,
                    "Variant SKU": item.get("code") + "_" + variant['color'] + "_" + variant['size'],
                    "Variant Inventory Qty": int(variant['quantity']),
                    "Variant Price": "$200",
                    "Variant Inventory Policy": "deny",
                    "Variant Requires Shipping": "TRUE",
                    "Variant Taxable": "TRUE",
                    "Variant Inventory Tracker": "shopify"
                }
                # Write the row to the CSV file
                writer.writerow(csv_row)

print('JSON data has been converted to CSV and written to csv')
