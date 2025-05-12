from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GameViewSet, GenreViewSet, GameRecommendationView

router = DefaultRouter()
router.register(r'games', GameViewSet)
router.register(r'genres', GenreViewSet)

urlpatterns = [
    path('games/recommend/', GameRecommendationView.as_view(), name='game-recommendation'),
    path('', include(router.urls)),
]
