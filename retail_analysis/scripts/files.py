import pandas as pd
import os

# Folders
csv_folder = 'data'   # folder containing CSVs
json_folder = 'static'  # folder to save JSON files

# Create JSON folder if it doesn't exist
os.makedirs(json_folder, exist_ok=True)

# Loop through all files in the CSV folder
for filename in os.listdir(csv_folder):
    if filename.endswith('.csv') and filename.lower() != 'transactions.csv':
        csv_path = os.path.join(csv_folder, filename)
        json_filename = filename.replace('.csv', '.json')
        json_path = os.path.join(json_folder, json_filename)

        # Read CSV and convert to JSON
        df = pd.read_csv(csv_path)
        df.to_json(json_path, orient='records', indent=4)

        print(f'✅ Converted {filename} → {json_filename}')
