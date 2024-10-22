import pandas as pd

# Load the first CSV file (sheet1)
sheet1_path = 'data/sheet1.csv'  # Replace with the actual file path
sheet1 = pd.read_csv(sheet1_path)

# Load the second CSV file (sheet2)
sheet2_path = 'data/sheet2.csv'  # Replace with the actual file path
sheet2 = pd.read_csv(sheet2_path)

# Merge the two sheets on the 'Style Code' column
merged_df = pd.merge(sheet1, sheet2, on='code', how='outer',
                     suffixes=('_sheet1', '_sheet2'))


# Create a new 'Max Price' column that takes the maximum of the prices from both sheets
merged_df['Price'] = merged_df[[
    'price_sheet1', 'price_sheet2']].max(axis=1)

# Select the necessary columns (Style Code and Max Price)
result_df = merged_df[['code', 'Price']]

# Save the result to a new CSV file
# Replace with your desired output file path
output_file_path = 'combined_prices.csv'
result_df.to_csv(output_file_path, index=False)

print(f"Combined data with max prices has been saved to {output_file_path}")
