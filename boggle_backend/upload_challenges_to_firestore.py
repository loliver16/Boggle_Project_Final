"""
Script to upload challenges from firestore_challenges.json to Firestore.
This ensures solutions are stored as arrays, not strings.
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

try:
    import firebase_admin
    from firebase_admin import credentials, firestore
except ImportError:
    print("Error: firebase-admin not installed. Install it with: pip3 install firebase-admin")
    sys.exit(1)

def initialize_firebase():
    """Initialize Firebase Admin SDK."""
    from django.conf import settings
    
    # Check if Firebase is already initialized
    if not firebase_admin._apps:
        # Try to get service account key path from settings
        service_account_path = getattr(settings, 'FIREBASE_SERVICE_ACCOUNT_KEY', None)
        
        if service_account_path and os.path.exists(service_account_path):
            cred = credentials.Certificate(service_account_path)
            firebase_admin.initialize_app(cred)
        else:
            # Try default location
            default_path = Path(__file__).parent / 'firebase-service-account.json'
            if default_path.exists():
                cred = credentials.Certificate(str(default_path))
                firebase_admin.initialize_app(cred)
            else:
                raise Exception(
                    "Firebase not configured. Please set FIREBASE_SERVICE_ACCOUNT_KEY in settings.py "
                    "or place firebase-service-account.json in the boggle_backend directory"
                )
    
    return firestore.client()

def upload_challenges():
    """Upload challenges from JSON file to Firestore."""
    # Load challenges from JSON file
    json_file = Path(__file__).parent / 'firestore_challenges.json'
    
    if not json_file.exists():
        print(f"Error: {json_file} not found!")
        print("Please run create_firestore_challenges.py first to generate the JSON file.")
        return
    
    print(f"Loading challenges from {json_file}...")
    with open(json_file, 'r') as f:
        challenges_data = json.load(f)
    
    print(f"Found {len(challenges_data)} challenges")
    
    # Initialize Firestore
    db = initialize_firebase()
    challenges_ref = db.collection('Challenges')
    
    # Upload each challenge
    for challenge_id, challenge_data in challenges_data.items():
        print(f"\nUploading {challenge_id}...")
        
        # Ensure solutions is an array (not a string)
        if 'solutions' in challenge_data:
            solutions = challenge_data['solutions']
            if isinstance(solutions, str):
                # Try to parse if it's a JSON string
                try:
                    solutions = json.loads(solutions)
                except json.JSONDecodeError:
                    print(f"  Warning: solutions is a string but not valid JSON")
                    continue
            elif not isinstance(solutions, list):
                print(f"  Warning: solutions is not a list or string, got {type(solutions)}")
                continue
            
            # Ensure all solutions are strings
            solutions = [str(word).strip().upper() for word in solutions if word]
            challenge_data['solutions'] = solutions
            print(f"  Solutions: {len(solutions)} words")
        
        # Ensure grid is correct format - Firestore doesn't support nested arrays
        # So we'll store grid as array of strings (each string is a row)
        if 'grid' in challenge_data:
            grid = challenge_data['grid']
            if isinstance(grid, list) and len(grid) > 0:
                # Ensure it's a 2D array
                if isinstance(grid[0], list):
                    # Convert 2D array to array of strings for Firestore
                    grid_as_strings = [''.join(row) for row in grid]
                    challenge_data['grid'] = grid_as_strings
                    print(f"  Grid: {len(grid)}x{len(grid[0])} (converted to array of strings)")
                else:
                    # Already array of strings, keep as-is
                    print(f"  Grid: already array of strings, length: {len(grid)}")
            else:
                print(f"  Warning: Grid is invalid, skipping")
                continue
        
        # Add/update metadata
        challenge_data['challenge_id'] = challenge_id
        challenge_data['isActive'] = True
        challenge_data['updatedAt'] = datetime.now().isoformat() + "Z"
        
        # Upload to Firestore
        doc_ref = challenges_ref.document(challenge_id)
        doc_ref.set(challenge_data, merge=False)  # Use merge=False to replace entire document
        
        print(f"  ✓ Uploaded successfully")
    
    print(f"\n✓ All challenges uploaded to Firestore!")
    print(f"Collection: Challenges")
    print(f"Total documents: {len(challenges_data)}")

if __name__ == "__main__":
    try:
        upload_challenges()
    except Exception as e:
        print(f"\nError: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
