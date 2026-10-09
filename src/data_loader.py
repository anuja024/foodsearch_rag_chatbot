import json
from pathlib import Path

def load_food_data(file_path):
    """Load food data from a JSON file."""
    
    file_path = Path(file_path)
    with open(file_path, 'r') as f:
        return json.load(f)
    return food_data

if __name__ == "__main__":
    data = load_food_data("data/FoodDataSet.json")

    print(f"Loaded {len(data)} food records.")
    print(data[0]["food_name"])