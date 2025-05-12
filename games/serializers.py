from rest_framework import serializers
from .models import Game, Genre

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']

class GameSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    genre_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Genre.objects.all(), write_only=True, source='genres'
    )

    class Meta:
        model = Game
        fields = ['id', 'name', 'description', 'storyline', 'release_date', 'rating', 'genres', 'genre_ids']
