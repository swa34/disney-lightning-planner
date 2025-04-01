import json
import os

# This script reads the data from resturant.json and saves it to the static folder
# as restaurants.json for the web application to use

# Read the restaurant data
with open('resturant.json', 'r', encoding='utf-8') as file:
    restaurant_data = json.load(file)

# Ensure the static directory exists
os.makedirs('static', exist_ok=True)

# Save the data to the static folder
with open('static/restaurants.json', 'w', encoding='utf-8') as file:
    json.dump(restaurant_data, file, indent=2)

print(f"Saved restaurant data to static/restaurants.json")