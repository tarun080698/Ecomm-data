import pandas as pd

# Load the data
file_path = 'products.csv'  # Replace with the correct path to your CSV file
df = pd.read_csv(file_path)

# Create a pivot table with Product Code as the index and Source Page as columns
pivot_df = df.pivot_table(
    index='Product Code', columns='Source Page', values='Product Price', aggfunc='first')

# Reset the index to make 'Product Code' a column again
pivot_df.reset_index(inplace=True)

# Merge the pivot table with the original DataFrame
merged_df = pd.merge(df, pivot_df, on='Product Code', how='left')

# Drop duplicates based on Product Code, keeping the first occurrence
final_df = merged_df.drop_duplicates(subset='Product Code', keep='first')

# Save the transformed DataFrame to a new CSV file
# Specify the path for the output file
output_file_path = 'transformed_products.csv'
final_df.to_csv(output_file_path, index=False)

print(f"Transformed data saved to {output_file_path}")


# Load the transformed data
# Specify the path to your transformed CSV file
transformed_file_path = 'transformed_products.csv'
df = pd.read_csv(transformed_file_path)

# Count the unique product codes
unique_product_codes_count = df['Product Code'].nunique()

print(f"Count of unique product codes: {unique_product_codes_count}")
