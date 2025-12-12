from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Games
from .serializers import GamesSerializer
from .firestore_service import (
    get_all_challenges,
    get_challenge_by_id,
    format_challenge_for_api
)
from .randomGen import random_grid
from .readJSONFile import read_json_to_list
from .boggle_solver import Boggle
from django.contrib.staticfiles import finders
from datetime import datetime
import json

# define the endpoints

@api_view(['GET', 'DELETE']) # define a GET Object with pk
def get_game(request, pk):
    try:
        game = Games.objects.get(pk=pk)
    except Games.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = GamesSerializer(game)
        return Response(serializer.data)
    elif request.method == 'DELETE':
        game.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
 
@api_view(['GET']) # define a GET REQUEST to get ALL Games
def get_games(request):
    games = Games.objects.all()
    serializer = GamesSerializer(games, many=True)
    return Response(serializer.data)

@api_view(['GET']) # define a GET REQUEST TO CREATE A SPECIFIC GAME OF SIZE size
def create_game(request, size):
    # Validate size
    if size < 3 or size > 10:
        return Response(
            {"error": "Size must be between 3 and 10 (inclusive)"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        g = random_grid(size)
        now = datetime.now()
        name = f'Rand{size}x{size}_{now.strftime("%Y%m%d%H%M%S")}'

        # Find the absolute path of the static JSON file
        file_path = finders.find("data/full-wordlist.json")
        
        if not file_path:
            return Response(
                {"error": "Dictionary file not found"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        dictionary = read_json_to_list(file_path)

        mygame = Boggle(g, dictionary)
        fwords = mygame.getSolution()

        # Serialize grid and foundwords as JSON strings
        grid_json = json.dumps(g)
        foundwords_json = json.dumps(fwords)

        serializer = GamesSerializer(data={
            "name": name,
            "size": size, 
            "grid": grid_json, 
            "foundwords": foundwords_json
        })
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(
            {"error": str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# Challenge endpoints - using Firestore
@api_view(['GET'])
def get_active_challenges(request):
    """Get all active challenges with their high scores from Firestore"""
    try:
        challenges = get_all_challenges()
        # Format each challenge for API response
        formatted_challenges = []
        for challenge in challenges:
            try:
                formatted = format_challenge_for_api(challenge)
                formatted_challenges.append(formatted)
            except Exception as e:
                print(f"Error formatting challenge {challenge.get('id', 'unknown')}: {str(e)}")
                continue
        
        return Response(formatted_challenges)
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Error in get_active_challenges: {str(e)}")
        print(error_details)
        return Response(
            {"error": str(e), "detail": "Failed to retrieve challenges from Firestore.", "traceback": error_details}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def get_challenge(request, challenge_id):
    """Get a specific challenge by ID from Firestore"""
    try:
        challenge = get_challenge_by_id(challenge_id)
        
        if not challenge:
            return Response(
                {"error": "Challenge not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Format challenge for API response
        formatted_challenge = format_challenge_for_api(challenge)
        return Response(formatted_challenge)
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Error in get_challenge: {str(e)}")
        print(error_details)
        return Response(
            {"error": str(e), "detail": "Failed to retrieve challenge from Firestore."}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )