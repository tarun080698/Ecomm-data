import json
import pandas as pd

# Load the JSON file
with open('glitterati_products.json', 'r') as json_file:
    json_data = json.load(json_file)

# Load the CSV file into a pandas DataFrame
csv_data = pd.read_csv('ecomm-all.csv')

# Extract the list of STYLE NO. from the CSV file
style_numbers = csv_data['STYLE NO.'].tolist()

# Filter the JSON data based on the code
filtered_data = [item for item in json_data if item.get(
    'code') in style_numbers]

# Save the filtered data to a new JSON file
with open('filtered_data_glitaratti.json', 'w') as output_file:
    json.dump(filtered_data, output_file, indent=4)

print('Filtered data has been written to filtered_data.json')
