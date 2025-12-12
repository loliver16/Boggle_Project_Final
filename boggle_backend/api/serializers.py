from rest_framework import serializers
from .models import Games
import json

# creating a model class below
class GamesSerializer(serializers.ModelSerializer):
    # Custom fields to handle JSON serialization/deserialization
    grid = serializers.CharField()
    foundwords = serializers.CharField()
    
    class Meta:
        model = Games
        fields = '__all__'
    
    def to_representation(self, instance):
        """Convert JSON strings to Python objects when reading"""
        representation = super().to_representation(instance)
        try:
            representation['grid'] = json.loads(representation['grid']) if representation.get('grid') else []
        except (json.JSONDecodeError, TypeError):
            representation['grid'] = []
        
        try:
            representation['foundwords'] = json.loads(representation['foundwords']) if representation.get('foundwords') else []
        except (json.JSONDecodeError, TypeError):
            representation['foundwords'] = []
        
        return representation
    
    def to_internal_value(self, data):
        """Ensure grid and foundwords are JSON strings when writing"""
        # If grid/foundwords are already strings (JSON), keep them
        # If they're lists/dicts, convert to JSON
        if 'grid' in data and isinstance(data['grid'], (list, dict)):
            data = data.copy()
            data['grid'] = json.dumps(data['grid'])
        
        if 'foundwords' in data and isinstance(data['foundwords'], (list, dict)):
            data = data.copy()
            data['foundwords'] = json.dumps(data['foundwords'])
        
        return super().to_internal_value(data)

# Note: Challenge and LeaderboardEntry serializers removed
# Challenges are now handled via Firestore in firestore_service.py