"""
Script to generate solutions for challenge grids.
Run this to populate the solutions array for each challenge.
"""

import sys
import os
import json
from pathlib import Path

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
    
    print(f"  Loading dictionary from: {file_path}")
    dictionary = read_json_to_list(str(file_path))
    print(f"  Dictionary loaded: {len(dictionary)} words")
    dictionary = [w.upper() for w in dictionary]  # Ensure uppercase to match solver
    print(f"  Dictionary after uppercase: {len(dictionary)} words (sample: {dictionary[:5]})")
    
    print(f"  Grid shape: {len(grid)}x{len(grid[0]) if grid else 0}")
    print(f"  Grid sample: {grid[0] if grid else 'empty'}")
    
    # Test grid validation manually
    print(f"  Testing grid validation...")
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            is_str = isinstance(cell, str)
            is_alpha = cell.isalpha() if is_str else False
            upper_cell = cell.upper() if is_str else None
            print(f"    Cell [{i}][{j}]: '{cell}' -> is_str={is_str}, is_alpha={is_alpha}, upper='{upper_cell}'")
            if not is_str or not is_alpha:
                print(f"      ❌ Invalid: not string or not alphabetic")
            elif upper_cell in ["Q", "S", "I"]:
                print(f"      ❌ Invalid: cell is '{upper_cell}' (Q/S/I not allowed)")
    
    mygame = Boggle(grid, dictionary)
    print(f"  Solver created, invalid_grid flag: {mygame.invalid_grid}")
    solutions = mygame.getSolution()
    print(f"  Solutions found: {len(solutions)} (sample: {solutions[:5] if solutions else 'none'})")
    return solutions


# --- Challenge Grids ---
CHALLENGES = {
    "challenge_timed_30s": {
        "grid": [
            ["R", "E", "T", "A"],
            ["L", "I", "N", "S"],
            ["O", "M", "E", "D"],
            ["P", "A", "R", "K"]
        ]
    },
    "challenge_timed_60s": {
        "grid": [
            ["C", "A", "R", "T"],
            ["H", "O", "M", "E"],
            ["S", "T", "A", "R"],
            ["P", "L", "A", "Y"]
        ]
    },
    "challenge_wordgoal_15": {
        "grid": [
            ["B", "E", "A", "T"],
            ["L", "O", "V", "E"],
            ["S", "O", "N", "G"],
            ["M", "U", "S", "E"]
        ]
    },
    "challenge_wordgoal_25": {
        "grid": [
            ["T", "H", "I", "N"],
            ["K", "W", "O", "R"],
            ["D", "A", "Y", "S"],
            ["M", "O", "O", "N"]
        ]
    },
    "challenge_combined_20words_90s": {
        "grid": [
            ["F", "L", "A", "M"],
            ["E", "D", "I", "T"],
            ["S", "O", "R", "T"],
            ["P", "A", "L", "E"]
        ]
    }
}

# --- Main ---
if __name__ == "__main__":
    import django
    from django.conf import settings
    
    if not settings.configured:
        settings.configure(
            DEBUG=True,
            STATIC_URL='/static/',
            STATICFILES_DIRS=[str(BASE_DIR / 'boggle_backend' / 'static')],
            INSTALLED_APPS=['django.contrib.staticfiles'],
        )
        django.setup()
    
    results = {}
    for challenge_id, data in CHALLENGES.items():
        print(f"Generating solutions for {challenge_id}...")
        grid = data["grid"]
        solutions = generate_solutions(grid)
        results[challenge_id] = {
            "grid": grid,
            "solutions": solutions,
            "word_count": len(solutions)
        }
        print(f"  Found {len(solutions)} words")
    
    output_file = Path(__file__).parent / 'challenge_solutions.json'
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nSolutions saved to {output_file}")
    print("\nWord counts:")
    for challenge_id, data in results.items():
        print(f"  {challenge_id}: {data['word_count']} words")
