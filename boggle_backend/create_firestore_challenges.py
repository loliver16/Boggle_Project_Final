"""
Script to create Firestore-ready challenge documents with all metadata.
"""

import sys
import os
import json
from pathlib import Path
from datetime import datetime

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'boggle_backend.settings')
sys.path.insert(0, str(Path(__file__).parent))

import django
django.setup()

from api.boggle_solver import Boggle
from api.readJSONFile import read_json_to_list
from django.contrib.staticfiles import finders

def generate_solutions(grid):
    """Generate all valid solutions for a given grid."""
    file_path = finders.find("data/full-wordlist.json")
    if not file_path:
        file_path = Path(__file__).parent / 'boggle_backend' / 'static' / 'data' / 'full-wordlist.json'
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Dictionary file not found at {file_path}")
    
    dictionary = read_json_to_list(str(file_path))
    mygame = Boggle(grid, dictionary)
    solutions = mygame.getSolution()
    return solutions

# Complete challenge definitions with metadata
CHALLENGES = {
    "challenge_timed_30s": {
        "name": "30-Second Speed Challenge",
        "description": "Find as many words as possible in just 30 seconds! Test your speed and word-finding skills.",
        "type": "time_limited",
        "timeLimit": 30,
        "wordGoal": None,
        "grid": [["R","E","T","A"], ["L","A","N","T"], ["O","M","E","D"], ["P","A","R","K"]]
    },
    "challenge_timed_60s": {
        "name": "60-Second Challenge",
        "description": "You have 60 seconds to find as many words as you can! More time means more opportunities.",
        "type": "time_limited",
        "timeLimit": 60,
        "wordGoal": None,
        "grid": [["C","A","R","T"], ["H","O","M","E"], ["T","T","A","R"], ["P","L","A","Y"]]
    },
    "challenge_wordgoal_15": {
        "name": "15-Word Goal Challenge",
        "description": "Can you find at least 15 valid words? Take your time and explore the board carefully.",
        "type": "word_goal",
        "timeLimit": None,
        "wordGoal": 15,
        "grid": [["B","E","A","T"], ["L","O","V","E"], ["T","O","N","G"], ["M","U","T","E"]]
    },
    "challenge_wordgoal_25": {
        "name": "25-Word Goal Challenge",
        "description": "A challenging goal: find at least 25 words! This requires careful exploration of the board.",
        "type": "word_goal",
        "timeLimit": None,
        "wordGoal": 25,
        "grid": [["T","H","A","N"], ["K","W","O","R"], ["D","A","Y","T"], ["M","O","O","N"]]
    },
    "challenge_combined_20words_90s": {
        "name": "20 Words in 90 Seconds",
        "description": "The ultimate challenge! Find at least 20 words within 90 seconds. Speed and accuracy required!",
        "type": "combined",
        "timeLimit": 90,
        "wordGoal": 20,
        "grid": [["F","L","A","M"], ["E","D","A","T"], ["T","O","R","T"], ["P","A","L","E"]]
    }
}

if __name__ == "__main__":
    print("Creating Firestore-ready challenge documents...\n")
    
    firestore_docs = {}
    
    for challenge_id, challenge_data in CHALLENGES.items():
        print(f"Processing {challenge_id}...")
        grid = challenge_data["grid"]
        
        try:
            solutions = generate_solutions(grid)
            print(f"  ✓ Found {len(solutions)} valid words")
            
            # Create Firestore document
            firestore_doc = {
                "id": challenge_id,
                "name": challenge_data["name"],
                "description": challenge_data["description"],
                "type": challenge_data["type"],
                "grid": grid,
                "solutions": solutions,
                "timeLimit": challenge_data["timeLimit"],
                "wordGoal": challenge_data["wordGoal"],
                "isActive": True,
                "createdAt": datetime.now().isoformat() + "Z"
            }
            
            firestore_docs[challenge_id] = firestore_doc
            
        except Exception as e:
            print(f"  ✗ Error: {str(e)}")
            import traceback
            traceback.print_exc()
    
    # Save Firestore-ready JSON
    output_file = Path(__file__).parent / 'firestore_challenges.json'
    with open(output_file, 'w') as f:
        json.dump(firestore_docs, f, indent=2)
    
    print(f"\n✓ Firestore documents saved to: {output_file}")
    print("\nSummary:")
    for challenge_id, doc in firestore_docs.items():
        print(f"  {challenge_id}: {len(doc['solutions'])} words")
