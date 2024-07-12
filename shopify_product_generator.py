import json
import csv

# Define the required headers for the CSV
headers = ["Handle", "Title", "Body (HTML)", "Description", "Vendor", "Type", "Option1 Name", "Option1 Value", "Option2 Name", "Option2 Value", "Variant SKU", "Variant Inventory Qty",
           "Variant Price", "Variant Inventory Policy", "Variant Requires Shipping", "Variant Taxable", "Image Src", "Variant Inventory Tracker"]

# Load the JSON file
with open('updated_data.json', 'r') as json_file:
    json_data = json.load(json_file)

# Open a new CSV file for writing
with open('DEMO_shopify_data_1.csv', 'w', newline='') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=headers)

    # Write the header row
    writer.writeheader()

    # Write the JSON data to the CSV file
    for index, item in enumerate(json_data):
        # Create a dictionary for the CSV row
        img = item["additional_images_url"][0]
        if "variants" in item.keys():
            for variant in item['variants']:
                csv_row = {
                    "Handle": item.get("code").lower(),
                    "Title": item.get("code") + " " + item.get("name"),
                    "Body (HTML)": item.get("description"),
                    "Description": item.get("description"),
                    "Vendor": "Milano Formals",
                    "Type": "Dress",
                    "Option1 Name": "Size",
                    "Option1 Value": variant['size'],
                    "Option2 Name": "Color",
                    "Option2 Value": variant['color'],
                    "Variant SKU": item.get("code") + "_" + variant['color'] + "_" + variant['size'],
                    "Variant Inventory Tracker": "shopify",
                    "Variant Inventory Qty": variant['quantity'],
                    "Variant Price": "$200",
                    "Variant Inventory Policy":  "deny",
                    "Variant Requires Shipping": "TRUE",
                    "Variant Taxable": "TRUE",
                    "Image Src": img,
                }
                # Write the row to the CSV file
                writer.writerow(csv_row)

print('JSON data has been converted to CSV and written to output.csv')
