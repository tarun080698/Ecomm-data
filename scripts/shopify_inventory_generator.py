import json
import csv

# Define the required headers for the new CSV
headers = ["Handle", "Title", "Option1 Name", "Option1 Value", "Option2 Name", "Option2 Value", "Option3 Name", "Option3 Value",
           "SKU", "HS Code", "COO", "Location", "Incoming", "Unavailable", "Committed", "Available", "On hand"]

# Load the JSON file
with open('test.json', 'r') as json_file:
    json_data = json.load(json_file)

# Open a new CSV file for writing
with open('csv_data/shopify_data_new.csv', 'w', newline='') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=headers)

    # Write the header row
    writer.writeheader()

    # Write the JSON data to the CSV file
    for index, item in enumerate(json_data):
        # Create a dictionary for the CSV row
        if "variants" in item.keys():
            for variant in item['variants']:
                csv_row = {
                    "Handle": item.get("code").lower(),
                    "Title": item.get("code") + " " + item.get("name"),
                    "Option1 Name": "Size",
                    "Option1 Value": variant['size'],
                    "Option2 Name": "Color",
                    "Option2 Value": variant['color'],
                    "SKU": item.get("code") + "_" + variant['color'] + "_" + variant['size'],
                    "HS Code": "",  # Add HS Code if available
                    "COO": "US",  # Add Country of Origin if available
                    # Assuming location is provided in the variant
                    "Location": variant.get("location", ""),
                    # Assuming incoming quantity is provided in the variant
                    "Incoming": variant.get("incoming", 0),
                    # Assuming unavailable quantity is provided in the variant
                    "Unavailable": variant.get("unavailable", 0),
                    # Assuming committed quantity is provided in the variant
                    "Committed": variant.get("committed", 0),
                    # Available quantity
                    "Available": variant.get("quantity", 0),
                    # Total quantity on hand
                    "On hand": variant.get("quantity", 0)
                }
                # Write the row to the CSV file
                writer.writerow(csv_row)

print('JSON data has been converted to CSV and written to DEMO_shopify_data_1.csv')
