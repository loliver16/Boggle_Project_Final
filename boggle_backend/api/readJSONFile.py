
import re
import sys
import json

def read_json_to_list(file_path):
    # Open and read the JSON file    
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
    # Extract only the "words" array from the JSON
    # The JSON structure is: {"source": "...", "words": [...]}
    if "words" in data and isinstance(data["words"], list):
        return data["words"]
    # Fallback: if structure is different, try to find any list value
    string_list = []
    for value in data.values():
        if isinstance(value, list):
            string_list.extend(value)
    return string_list