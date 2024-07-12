import pandas as pd

# Load the original CSV file
df = pd.read_csv("Ecom_data.csv")

# Ensure QUANTITY is numeric, coercing errors to NaN
df['QUANTITY'] = pd.to_numeric(df['QUANTITY'], errors='coerce')

# Fill NaN values in QUANTITY with 0 (or handle as needed)
df['QUANTITY'] = df['QUANTITY'].fillna(0)

# First aggregation: Sum quantities based on STYLE NO., COLOR, and SIZE
aggregated_df = df.groupby(['STYLE NO.', 'COLOR', 'SIZE', 'BOX NUMBER'], as_index=False).agg({
    'BRAND NAME': 'first',
    'QUANTITY': 'sum'
})

# Second aggregation: Sum quantities based on STYLE NO. to get total quantity for each style
style_quantity_df = aggregated_df.groupby('STYLE NO.', as_index=False).agg({
    'QUANTITY': 'sum'
})

# Sort by QUANTITY in descending order and select the top 50 styles
top_50_styles = style_quantity_df.sort_values(
    by='QUANTITY', ascending=False).head(50)['STYLE NO.']

# Filter the original aggregated DataFrame to include only rows corresponding to the top 50 styles
top_50_df = aggregated_df[aggregated_df['STYLE NO.'].isin(top_50_styles)]

# Write the result to a new CSV file
top_50_df.to_csv('csv_data/top_50_products_new.csv', index=False)

print('The top 50 unique styles based on quantity have been written to top_50_products.csv')
