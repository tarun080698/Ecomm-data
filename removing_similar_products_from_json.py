import json

# Load the first JSON file
with open('filtered_data_glitaratti.json', 'r') as json_file1:
    data1 = json.load(json_file1)

# Load the second JSON file
with open('filtered_data.json', 'r') as json_file2:
    data2 = json.load(json_file2)

# Create a dictionary to keep track of unique entries based on the "code" key
merged_data_dict = {}

# Add data from the first JSON file to the dictionary
for item in data1:
    merged_data_dict[item['code']] = item

# Add data from the second JSON file to the dictionary, avoiding duplicates
count = 0
for item in data2:
    if item['code'] not in merged_data_dict:
        merged_data_dict[item['code']] = item
    else:
        count += 1
        # print(item['code'])

print(count)
# Convert the dictionary back to a list
merged_data = list(merged_data_dict.values())

# Write the merged data to a new JSON file
with open('merged_data_products.json', 'w') as output_file:
    json.dump(merged_data, output_file, indent=4)

print('Merged data has been written to merged_data.json')
