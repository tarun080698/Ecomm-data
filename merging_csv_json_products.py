import json
import pandas as pd

# Load the JSON file
with open('our_products_new.json', 'r') as json_file:
    json_data = json.load(json_file)

# Load the CSV file into a pandas DataFrame
csv_data = pd.read_csv('csv_data/top_50_products_new.csv')

count = 0
# Iterate over the CSV rows and update the JSON data
for _, row in csv_data.iterrows():
    style_no = row['STYLE NO.']
    color = row['COLOR']
    size = row['SIZE']
    quantity = row['QUANTITY']
    location = row['BOX NUMBER']

    # Find the matching dict in the JSON data
    for item in json_data:
        # print(item.get('code'), style_no)

        if item.get('code') == style_no:
            if 'variants' not in item:
                item['variants'] = []
            # Add the color, size, and quantity as a new variant
            item['variants'].append({
                'color': color,
                'size': size,
                'quantity': quantity,
                "location": location
            })

        # else:
        #     print(item.get('code'))

# # Save the updated list of dicts to a new JSON file
with open('test.json', 'w') as output_file:
    json.dump(json_data, output_file, indent=4)

print('Updated data has been written to updated_data.json')
