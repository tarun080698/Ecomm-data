import json

def read_json_file(file_path):
    """Read JSON data from a file and return it as a Python object."""
    with open(file_path, 'r') as file:
        return json.load(file)

def write_json_file(file_path, data):
    """Write a Python object as JSON to a file."""
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def merge_json_files(file1, file2, output_file):
    """Merge two JSON files based on the 'code' in the array of objects."""
    data1 = read_json_file(file1)
    data2 = read_json_file(file2)

    # Use a dictionary to store unique products based on the 'code'
    merged_data = {}

    # Function to add items to the merged data
    def add_to_merged_data(items):
        for item in items:
            code = item['code']
            merged_data[code] = item

    # Add items from both JSON files
    add_to_merged_data(data1)
    add_to_merged_data(data2)

    # Convert the dictionary back to a list
    merged_list = list(merged_data.values())

    # Write the merged list to the output file
    write_json_file(output_file, merged_list)

# Example usage
file1 = 'bella_sposa_products.json'  # Path to the first JSON file
file2 = 'glitterati_products.json'  # Path to the second JSON file
output_file = 'merged.json'  # Path to the output JSON file

merge_json_files(file1, file2, output_file)
