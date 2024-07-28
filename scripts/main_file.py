import json
import csv

# Define the required headers for the CSV
headers = [
    "Handle", "Title", "Body (HTML)", "Description", "Vendor", "Type", "Option1 Name",
    "Option1 Value", "Option2 Name", "Option2 Value", "Variant SKU", "Variant Inventory Qty",
    "Variant Price", "Variant Inventory Policy", "Variant Requires Shipping", "Variant Taxable",
    "Image Src", "Image Position", "Image Alt Text", "Variant Inventory Tracker"
]

# Load the JSON file
with open('data/updated_data.json', 'r') as json_file:
    json_data = json.load(json_file)

# Open a new CSV file for writing
with open('data/shopify_data_1.csv', 'w', newline='') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=headers)

    # Write the header row
    writer.writeheader()

    # Write the JSON data to the CSV file
    for item in json_data:
        handle = item.get("code").lower()
        title = item.get("code") + " " + item.get("name")
        description = item.get("Long Description")
        keywords = item.get("Keywords")
        body_html = f'<p>{description}</p>\n<ul>'
        for i in range(1,len(keywords)-1):
            body_html += f'\n<li>{keywords[i]}</li>'
        body_html += '\n</ul>'
        vendor = "Milano Formals"
        product_type = "Dress"

        # Track image position for each variant
        image_position = 1

        if "variants" in item.keys():
            for variant in item['variants']:
                csv_row = {
                    "Handle": handle,
                    "Title": title,
                    "Body (HTML)": body_html,

                    "Description": description,
                    "Vendor": vendor,
                    "Type": product_type,
                    "Option1 Name": "Size",
                    "Option1 Value": variant['size'],
                    "Option2 Name": "Color",
                    "Option2 Value": variant['color'],
                    "Variant SKU": f"{item.get('code')}_{variant['color']}_{variant['size']}",
                    "Variant Inventory Tracker": "shopify",
                    "Variant Inventory Qty": variant['quantity'],
                    "Variant Price": "$200",
                    "Variant Inventory Policy": "deny",
                    "Variant Requires Shipping": "TRUE",
                    "Variant Taxable": "TRUE",
                }

                # Write each variant row without image info first
                writer.writerow(csv_row)

                # Add rows for each image
                for img in item["additional_images_url"]:
                    csv_image_row = {
                        "Handle": handle,
                        "Title": '',
                        "Body (HTML)": '',
                        "Description": '',
                        "Vendor": '',
                        "Type": '',
                        "Option1 Name": '',
                        "Option1 Value": '',
                        "Option2 Name": '',
                        "Option2 Value": '',
                        "Variant SKU": '',
                        "Variant Inventory Tracker": '',
                        "Variant Inventory Qty": '',
                        "Variant Price": '',
                        "Variant Inventory Policy": '',
                        "Variant Requires Shipping": '',
                        "Variant Taxable": '',
                        "Image Src": img,
                        "Image Position": image_position,
                        "Image Alt Text": f"{title} - Image {image_position}",
                    }

                    # Write the image row
                    writer.writerow(csv_image_row)

                    # Increment image position
                    image_position += 1

print('JSON data has been converted to CSV and written to shopify_data_1.csv')
