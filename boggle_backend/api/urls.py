from django.urls import path
from .views import get_game, get_games, create_game, get_active_challenges, get_challenge

urlpatterns = [
    path('game/<int:pk>', get_game, name='get_game'),
    path('games/', get_games, name='get_games'),
    path('game/create/<int:size>', create_game, name='create_game'),
    
    # Challenge endpoints
    path('challenges/', get_active_challenges, name='get_active_challenges'),
    path('challenges/<str:challenge_id>', get_challenge, name='get_challenge'),
]