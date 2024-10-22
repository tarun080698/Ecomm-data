# import pandas as pd


# def extract_code_from_filename(csv_file_path):
#     # Load the CSV file into a pandas DataFrame
#     df = pd.read_csv(csv_file_path)

#     # Extract the code (everything before the first underscore) from the 'file_name' column
#     df['Code'] = df['file_name'].apply(lambda x: x.split('_')[0])

#     # Save the modified DataFrame back to the CSV file (overwrite the original)
#     df.to_csv(csv_file_path, index=False)
#     print(f"Updated CSV file saved: {csv_file_path}")


# # Specify the path to your CSV file
# csv_file_path = "data/extras/shopify_urls.csv"

# # Call the function to extract the code and save it to a new column
# extract_code_from_filename(csv_file_path)


b = 'https://cdn.shopify.com/s/files/1/0649/4820/7797/files/B8998_Sangria_3.png?v=1727407844'
bc = b.split("_")
print(len(bc))
print(bc[1])
