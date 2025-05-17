from django.contrib import admin
from .models import Game, Genre

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'release_date', 'rating')
    search_fields = ('name', 'description', 'storyline')
    list_filter = ('release_date', 'rating', 'genres')
    filter_horizontal = ('genres',)

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
