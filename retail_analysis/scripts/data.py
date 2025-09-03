import pandas as pd
import json
import os

# Define file paths relative to your project folder
base_dir = r"C:\Users\saisr\Desktop\retail_analysis"
data_file = os.path.join(base_dir, "data", "transactions.csv")
output_dir = os.path.join(base_dir, "outputs")

# Create outputs folder if not exists
os.makedirs(output_dir, exist_ok=True)

# 1. Load and clean dataset
df = pd.read_csv(data_file)

# Drop duplicates
df.drop_duplicates(inplace=True)

# Handle missing values
df.fillna({'Quantity': 0, 'Price': 0}, inplace=True)

# Fix data types

df['Quantity'] = df['Quantity'].astype(int)
df['Price'] = df['Price'].astype(float)

# Create TotalAmount column
df['TotalAmount'] = df['Quantity'] * df['Price']

# 2. Exploratory analysis
print(df.info())
print(df.describe())
print(df.isna().sum())
print(list(df.columns))
print(df.head())


# 3. Required calculations
top_products = df.groupby('ProductID')['Quantity'].sum().nlargest(5).reset_index()
print(top_products)
top_customers = df.groupby('CustomerID')['TotalAmount'].sum().nlargest(5).reset_index()
print(top_customers)
avg_purchase = df['TotalAmount'].mean()
print(avg_purchase)
customer_freq = df['CustomerID'].value_counts().reset_index()
print(customer_freq)
customer_freq.columns = ['CustomerID', 'Frequency']
print(customer_freq.columns)
category_revenue = df.groupby('ProductCategory')['TotalAmount'].sum().sort_values(ascending=False).reset_index()
print(category_revenue)
print(df['TotalAmount'].sum())


# Helper to export CSV only if not exists
def export_csv_if_not_exists(df, filename):
    filepath = os.path.join(output_dir, filename)
    if not os.path.exists(filepath):
        df.to_csv(filepath, index=False)
        print(f"Created: {filename}")
    else:
        print(f"Skipped (already exists): {filename}")

# 4. Export results (conditionally)
export_csv_if_not_exists(top_products, 'top_products.csv')
export_csv_if_not_exists(top_customers, 'top_customers.csv')
export_csv_if_not_exists(customer_freq, 'customer_frequency.csv')
export_csv_if_not_exists(category_revenue, 'category_revenue.csv')

# Export summary JSON
summary_file = os.path.join(output_dir, "summary.json")
if not os.path.exists(summary_file):
    results = {
        'avg_purchase': avg_purchase,
        'top_products': top_products.to_dict(orient='records'),
        'top_customers': top_customers.to_dict(orient='records'),
        'customer_frequency': customer_freq.to_dict(orient='records'),
        'category_revenue': category_revenue.to_dict(orient='records')
    }
    with open(summary_file, 'w') as f:
        json.dump(results, f, indent=4)
    print("Created: summary.json")
else:
    print("Skipped (already exists): summary.json")

print("All tasks complete.")
