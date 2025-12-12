"""
Firestore service for interacting with Firebase Firestore database.
Handles challenges and leaderboard data.
"""

import os
from pathlib import Path
from typing import List, Dict, Optional
from django.conf import settings

# Try to import Firebase Admin SDK
try:
    import firebase_admin
    from firebase_admin import credentials, firestore
    FIREBASE_AVAILABLE = True
except ImportError:
    FIREBASE_AVAILABLE = False
    firebase_admin = None

# Global Firestore client
_db = None


def get_firestore_client():
    """Initialize and return Firestore client."""
    global _db
    
    if not FIREBASE_AVAILABLE:
        raise Exception(
            "firebase-admin is not installed. Please install it with: pip3 install firebase-admin"
        )
    
    if _db is not None:
        return _db
    
    # Check if Firebase is already initialized
    if not firebase_admin._apps:
        # Try to get service account key path from settings
        service_account_path = getattr(settings, 'FIREBASE_SERVICE_ACCOUNT_KEY', None)
        
        if service_account_path and os.path.exists(service_account_path):
            cred = credentials.Certificate(service_account_path)
            firebase_admin.initialize_app(cred)
        else:
            # Try default location
            default_path = Path(__file__).parent.parent / 'firebase-service-account.json'
            if default_path.exists():
                cred = credentials.Certificate(str(default_path))
                firebase_admin.initialize_app(cred)
            else:
                # Use Application Default Credentials (for production/GCP)
                try:
                    firebase_admin.initialize_app()
                except Exception as e:
                    raise Exception(
                        f"Firebase not configured. Error: {str(e)}\n"
                        "Please either:\n"
                        "1. Set FIREBASE_SERVICE_ACCOUNT_KEY in settings.py to the path of your service account key\n"
                        "2. Place firebase-service-account.json in the boggle_backend directory\n"
                        "3. Use Application Default Credentials in a GCP environment"
                    ) from e
    
    _db = firestore.client()
    return _db


def get_all_challenges() -> List[Dict]:
    """Get all active challenges from Firestore."""
    db = get_firestore_client()
    challenges_ref = db.collection('Challenges')
    
    # Get all challenges first (to see what we have)
    all_docs = list(challenges_ref.stream())
    print(f"Total challenges in Firestore: {len(all_docs)}")
    
    # Debug: print first document structure if any exist
    if all_docs:
        first_doc = all_docs[0]
        first_data = first_doc.to_dict()
        print(f"Sample document ID: {first_doc.id}")
        print(f"Sample document fields: {list(first_data.keys())}")
        print(f"Sample isActive value: {first_data.get('isActive')} (type: {type(first_data.get('isActive'))})")
    
    # Filter for active challenges - check multiple possible field names and values
    active_docs = []
    for doc in all_docs:
        data = doc.to_dict()
        # Check multiple possible field names and values
        is_active = (
            data.get('isActive') == True or 
            data.get('isActive') == 'true' or
            data.get('isActive') == 'True' or
            data.get('is_active') == True or
            data.get('is_active') == 'true' or
            data.get('is_active') == 'True' or
            # If field doesn't exist, assume active (for backwards compatibility)
            ('isActive' not in data and 'is_active' not in data)
        )
        if is_active:
            active_docs.append(doc)
    
    print(f"Found {len(active_docs)} active challenges after filtering")
    
    challenges = []
    for doc in active_docs:
        try:
            challenge_data = doc.to_dict()
            challenge_data['id'] = doc.id
            # Add high score if leaderboard exists (wrap in try-except to handle errors)
            try:
                challenge_data['high_score'] = get_challenge_high_score(doc.id)
            except Exception as e:
                print(f"Warning: Could not get high score for {doc.id}: {str(e)}")
                challenge_data['high_score'] = None
            challenges.append(challenge_data)
        except Exception as e:
            print(f"Error processing challenge document {doc.id}: {str(e)}")
            continue
    
    # Sort by createdAt if available (descending, newest first)
    def get_created_at(challenge):
        try:
            created_at = challenge.get('createdAt') or challenge.get('created_at')
            if created_at:
                # Handle both timestamp and string formats
                if hasattr(created_at, 'timestamp'):
                    return created_at.timestamp()
                elif isinstance(created_at, str):
                    from datetime import datetime
                    try:
                        return datetime.fromisoformat(created_at.replace('Z', '+00:00')).timestamp()
                    except:
                        return 0
            return 0
        except Exception:
            return 0
    
    try:
        challenges.sort(key=get_created_at, reverse=True)
    except Exception as e:
        print(f"Warning: Could not sort challenges: {str(e)}")
    
    return challenges


def get_challenge_by_id(challenge_id: str) -> Optional[Dict]:
    """Get a specific challenge by ID."""
    db = get_firestore_client()
    doc_ref = db.collection('Challenges').document(challenge_id)
    doc = doc_ref.get()
    
    if doc.exists:
        challenge_data = doc.to_dict()
        challenge_data['id'] = doc.id
        
        # Debug: Print challenge data for troubleshooting
        print(f"DEBUG: Retrieved challenge {challenge_id}")
        print(f"DEBUG: Challenge fields: {list(challenge_data.keys())}")
        grid_raw = challenge_data.get('grid') or challenge_data.get('array')
        print(f"DEBUG: Grid field type: {type(challenge_data.get('grid'))}, Grid value: {str(challenge_data.get('grid'))[:200] if challenge_data.get('grid') else 'None'}")
        if 'array' in challenge_data:
            print(f"DEBUG: Array field type: {type(challenge_data.get('array'))}, Array value: {str(challenge_data.get('array'))[:200] if challenge_data.get('array') else 'None'}")
        
        # Add high score
        challenge_data['high_score'] = get_challenge_high_score(challenge_id)
        return challenge_data
    else:
        print(f"DEBUG: Challenge {challenge_id} not found in Firestore")
    return None


def get_challenge_high_score(challenge_id: str) -> Optional[Dict]:
    """Get the highest score for a challenge from leaderboard."""
    try:
        db = get_firestore_client()
        leaderboard_ref = db.collection('leaderboards').document(challenge_id).collection('entries')
        
        # Get top entry ordered by score descending, then by time_taken ascending
        try:
            query = leaderboard_ref.order_by('score', direction=firestore.Query.DESCENDING).order_by('timeTaken').limit(1)
            docs = list(query.stream())
        except Exception as e:
            # If ordering fails (maybe index missing), try just by score
            print(f"Warning: Could not order leaderboard by score and timeTaken: {str(e)}")
            try:
                query = leaderboard_ref.order_by('score', direction=firestore.Query.DESCENDING).limit(1)
                docs = list(query.stream())
            except Exception as e2:
                # If that fails, just get all entries and sort in Python
                print(f"Warning: Could not order leaderboard: {str(e2)}, getting all entries")
                docs = list(leaderboard_ref.stream())
                if docs:
                    # Sort in Python
                    docs.sort(key=lambda d: d.to_dict().get('score', 0), reverse=True)
                    docs = docs[:1]
        
        if docs:
            top_entry = docs[0].to_dict()
            return {
                'score': top_entry.get('score', 0),
                'username': top_entry.get('username', ''),
                'words_found': top_entry.get('wordsFound', 0)
            }
        return None
    except Exception as e:
        # If leaderboard doesn't exist or any other error, return None
        print(f"Error getting high score for {challenge_id}: {str(e)}")
        return None


def get_challenge_leaderboard(challenge_id: str, limit: int = 100) -> List[Dict]:
    """Get leaderboard entries for a challenge."""
    db = get_firestore_client()
    leaderboard_ref = db.collection('leaderboards').document(challenge_id).collection('entries')
    
    query = leaderboard_ref.order_by('score', direction=firestore.Query.DESCENDING).order_by('timeTaken').limit(limit)
    docs = query.stream()
    
    entries = []
    for doc in docs:
        entry_data = doc.to_dict()
        entry_data['id'] = doc.id
        entries.append(entry_data)
    
    return entries


def format_challenge_for_api(challenge_data: Dict) -> Dict:
    """Format challenge data from Firestore to match API response format."""
    import json
    import re
    
    challenge_id = challenge_data.get('id') or challenge_data.get('challenge_id', 'unknown')
    
    # Handle both camelCase and snake_case field names
    # Check multiple possible field names for grid (sometimes it might be stored under different names)
    grid = challenge_data.get('grid') or challenge_data.get('array') or challenge_data.get('board') or challenge_data.get('Grid') or []
    solutions = challenge_data.get('solutions', [])
    
    # If grid is still missing, log all available fields for debugging
    if not grid or (isinstance(grid, list) and len(grid) == 0):
        print(f"WARNING [{challenge_id}]: Grid field not found or empty. Available fields: {list(challenge_data.keys())}")
        # Check if 'array' field exists and might be the grid
        if 'array' in challenge_data:
            print(f"WARNING [{challenge_id}]: Found 'array' field, type: {type(challenge_data.get('array'))}, value: {str(challenge_data.get('array'))[:200]}")
            # Try using array as grid
            grid = challenge_data.get('array', [])
    
    print(f"DEBUG [{challenge_id}]: Raw grid type: {type(grid)}, length: {len(grid) if isinstance(grid, (list, str)) else 'N/A'}")
    if isinstance(grid, list) and len(grid) > 0:
        print(f"DEBUG [{challenge_id}]: First grid element type: {type(grid[0])}, value: {grid[0] if len(str(grid[0])) < 50 else str(grid[0])[:50]}")
    elif grid is None:
        print(f"DEBUG [{challenge_id}]: Grid is None!")
    elif grid == []:
        print(f"DEBUG [{challenge_id}]: Grid is empty list!")
    
    # Handle grid - might be string, list, or already formatted
    if isinstance(grid, str):
        try:
            grid = json.loads(grid)
            print(f"Parsed grid from JSON string")
        except json.JSONDecodeError:
            # If it's a string representation of an array, try to extract letters
            print(f"Warning: Grid is a string but not valid JSON, trying to extract letters")
            # Extract all letters and assume square grid
            letters = re.findall(r'[A-Za-z]', grid)
            if letters:
                grid_size = int(len(letters) ** 0.5)
                if grid_size * grid_size == len(letters):
                    grid = [[letters[i * grid_size + j].upper() for j in range(grid_size)] for i in range(grid_size)]
                    print(f"Extracted {grid_size}x{grid_size} grid from string")
                else:
                    grid = []
            else:
                grid = []
    elif not isinstance(grid, list):
        print(f"Warning: Grid is not a list, got {type(grid)}, value: {str(grid)[:100]}")
        grid = []
    
    # Convert grid to 2D array if needed
    if grid and len(grid) > 0:
        if not isinstance(grid[0], list):
            # Grid is a 1D array - try to convert to 2D
            # If first element is a string, assume each element is a row string
            if isinstance(grid[0], str):
                print(f"DEBUG [{challenge_id}]: Converting 1D array of strings to 2D array")
                # Clean each row string - remove quotes, brackets, commas, and spaces, keep only letters
                grid = [[char.upper() for char in re.sub(r'[^A-Za-z]', '', row)] for row in grid]
                # Filter out empty rows
                grid = [row for row in grid if row]
                print(f"DEBUG [{challenge_id}]: After conversion, grid has {len(grid)} rows")
            else:
                # Try to determine grid size (assume square grid)
                # Calculate size from total length
                total_chars = sum(len(str(item)) for item in grid) if grid else 0
                grid_size = int(total_chars ** 0.5)
                if grid_size * grid_size == total_chars:
                    # Flatten and reshape
                    flat = []
                    for item in grid:
                        flat.extend(list(str(item)))
                    grid = [flat[i:i+grid_size] for i in range(0, len(flat), grid_size)]
                    print(f"DEBUG [{challenge_id}]: Reshaped 1D array to {grid_size}x{grid_size} grid")
                else:
                    print(f"WARNING [{challenge_id}]: Cannot convert grid to 2D array. First element type: {type(grid[0])}, first value: {grid[0][:50] if isinstance(grid[0], str) else grid[0]}")
                    print(f"WARNING [{challenge_id}]: Total chars: {total_chars}, calculated size: {grid_size}")
                    grid = []
        else:
            # Already a 2D array, but make sure inner arrays contain strings/characters
            # Clean each cell - convert to string, uppercase, and filter out non-letter characters
            grid = [[re.sub(r'[^A-Za-z]', '', str(cell).upper()) for cell in row] for row in grid]
            # Filter out empty cells from rows (though this shouldn't happen)
            grid = [[cell for cell in row if cell] for row in grid]
            # Filter out empty rows
            grid = [row for row in grid if row]
            print(f"DEBUG [{challenge_id}]: Cleaned 2D array, final shape: {len(grid)}x{len(grid[0]) if grid else 0}")
    else:
        print(f"ERROR [{challenge_id}]: Grid is empty or None after parsing! Original: {challenge_data.get('grid', 'missing')}")
    
    # Handle solutions - might be string, list, or already formatted
    print(f"DEBUG [{challenge_id}]: Raw solutions type: {type(solutions)}, length: {len(solutions) if isinstance(solutions, (list, str)) else 'N/A'}")
    if isinstance(solutions, str):
        try:
            solutions = json.loads(solutions)
            print(f"DEBUG [{challenge_id}]: Parsed solutions from JSON string, length: {len(solutions) if isinstance(solutions, list) else 'N/A'}")
        except json.JSONDecodeError:
            print(f"WARNING [{challenge_id}]: Solutions is a string but not valid JSON")
            solutions = []
    elif isinstance(solutions, list):
        # Check if it's a list containing a JSON string (common Firestore storage format)
        if len(solutions) == 1 and isinstance(solutions[0], str):
            string_value = solutions[0]
            print(f"DEBUG [{challenge_id}]: Solutions is a list with one string element, length: {len(string_value)}, value preview: {string_value[:100] if string_value else 'EMPTY'}")
            
            # Check if it's an empty string
            if not string_value or not string_value.strip():
                print(f"ERROR [{challenge_id}]: Solutions list contains an empty string! Firestore data is corrupted.")
                solutions = []
            else:
                # Might be a JSON string inside a list - try to parse it
                try:
                    parsed = json.loads(string_value)
                    if isinstance(parsed, list):
                        print(f"DEBUG [{challenge_id}]: Solutions was a list containing a JSON string, parsed to {len(parsed)} items")
                        solutions = parsed
                    else:
                        print(f"DEBUG [{challenge_id}]: Solutions list[0] is a string but not a JSON array, type: {type(parsed)}")
                        solutions = []
                except (json.JSONDecodeError, TypeError) as e:
                    # Not JSON, might just be a regular string or the actual data
                    print(f"DEBUG [{challenge_id}]: Solutions is a list with one string element (not JSON), parse error: {e}")
                    print(f"DEBUG [{challenge_id}]: Trying to treat as comma-separated or split by spaces...")
                    # Try splitting by common delimiters if it looks like a list
                    if ',' in string_value:
                        solutions = [w.strip() for w in string_value.split(',') if w.strip()]
                        print(f"DEBUG [{challenge_id}]: Split by comma, got {len(solutions)} items")
                    else:
                        solutions = []
        # If it's already a list of strings/items, continue with it
    else:
        print(f"WARNING [{challenge_id}]: Solutions is not a list or string, got {type(solutions)}, value: {str(solutions)[:200] if solutions else 'None'}")
        solutions = []
    
    # Filter out empty strings, None values, and ensure all are strings
    if isinstance(solutions, list):
        original_count = len(solutions)
        solutions = [str(word).strip().upper() for word in solutions if word and str(word).strip()]
        if len(solutions) != original_count:
            print(f"DEBUG [{challenge_id}]: Filtered solutions from {original_count} to {len(solutions)} (removed empty/None values)")
    
    print(f"DEBUG [{challenge_id}]: Final solutions count: {len(solutions) if isinstance(solutions, list) else 0}")
    if isinstance(solutions, list) and len(solutions) > 0:
        print(f"DEBUG [{challenge_id}]: Sample solutions (first 5): {solutions[:5]}")
    elif isinstance(solutions, list) and len(solutions) == 0:
        print(f"ERROR [{challenge_id}]: Solutions array is empty! This will cause validation issues.")
    print(f"DEBUG [{challenge_id}]: Final formatted grid type: {type(grid)}, length: {len(grid) if grid else 0}, is 2D: {grid and len(grid) > 0 and isinstance(grid[0], list) if grid else False}")
    
    return {
        "id": challenge_data.get('id'),
        "challenge_id": challenge_data.get('id') or challenge_data.get('challenge_id'),
        "name": challenge_data.get('name'),
        "description": challenge_data.get('description'),
        "challenge_type": challenge_data.get('type'),  # Firestore uses 'type'
        "time_limit": challenge_data.get('timeLimit') or challenge_data.get('time_limit'),  # Handle both cases
        "word_goal": challenge_data.get('wordGoal') or challenge_data.get('word_goal'),  # Handle both cases
        "grid": grid,
        "solutions": solutions,
        "high_score": challenge_data.get('high_score')
    }
