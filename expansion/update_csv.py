import json

import pandas as pd

# Load your CSV (replace with your actual path)
df = pd.read_csv("circuit.csv")  # This should contain the 'name' column
df.drop("description", axis=1, inplace=True)  # Drop if exists

# Load the JSON (replace with your actual path)
with open("circuit_links.json", "r", encoding="utf-8") as f:
    json_data = json.load(f)

# Convert JSON to a DataFrame
json_df = pd.DataFrame.from_dict(json_data, orient="index").reset_index()

json_df.rename(columns={"index": "name", "intro": "description"}, inplace=True)

# Merge on the 'name' column
merged_df = df.merge(json_df[["name", "description"]], on="name", how="left")

# If you want to preview
print(merged_df.head())

# Save the updated dataframe (optional)
merged_df.to_csv("updated_data.csv", index=False)
