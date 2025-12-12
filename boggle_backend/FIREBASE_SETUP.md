# Firebase Setup Guide

## Step 1: Install Firebase Admin SDK

Install the Firebase Admin SDK for Python:

```bash
pip3 install firebase-admin
```

Or add to your requirements.txt:
```
firebase-admin
```

## Step 2: Get Firebase Service Account Key

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Select your project
3. Go to **Project Settings** (gear icon) → **Service Accounts**
4. Click **"Generate new private key"**
5. Save the JSON file securely

## Step 3: Place Service Account Key

You have two options:

### Option A: Default Location (Recommended for Development)
Place the service account JSON file in the `boggle_backend` directory and name it:
```
boggle_backend/firebase-service-account.json
```

### Option B: Custom Location
1. Place the file anywhere on your system
2. Update `boggle_backend/boggle_backend/settings.py`:
   ```python
   FIREBASE_SERVICE_ACCOUNT_KEY = '/path/to/your/firebase-service-account.json'
   ```

## Step 4: Firestore Structure

Make sure your Firestore has the following structure:

### Collection: `challenges`
Each document should have:
- `id` (string)
- `name` (string)
- `description` (string)
- `type` (string): "time_limited", "word_goal", or "combined"
- `grid` (array): 2D array of letters
- `solutions` (array): Array of valid words
- `timeLimit` (number or null)
- `wordGoal` (number or null)
- `isActive` (boolean)
- `createdAt` (timestamp or string)

### Collection: `leaderboards`
Each document ID should be a challenge ID, containing a subcollection `entries`:
- Document: `{challenge_id}`
  - Subcollection: `entries`
    - Each entry document should have:
      - `userId` (string)
      - `username` (string)
      - `score` (number)
      - `wordsFound` (number)
      - `words` (array)
      - `timeTaken` (number)
      - `submittedAt` (timestamp)

## Step 5: Test the Integration

1. Start your Django server:
   ```bash
   python3 manage.py runserver
   ```

2. Test the API endpoint:
   ```bash
   curl http://localhost:8000/api/challenges/
   ```

3. You should see your challenges from Firestore!

## Troubleshooting

### Error: "Firebase not configured"
- Make sure `firebase-service-account.json` exists in the correct location
- Or set `FIREBASE_SERVICE_ACCOUNT_KEY` in settings.py

### Error: "Permission denied"
- Check that your service account key has Firestore read permissions
- In Firebase Console, go to IAM & Admin → Service Accounts
- Ensure the service account has "Cloud Datastore User" role

### Error: "Collection not found"
- Verify that your Firestore collection is named `challenges` (case-sensitive)
- Check that documents exist in the collection
- Ensure documents have `isActive: true` for active challenges

## Security Note

⚠️ **Never commit your service account key to version control!**

Add to `.gitignore`:
```
firebase-service-account.json
*.json
!package.json
!package-lock.json
```
