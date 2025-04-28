from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GameViewSet
from .views import GenreViewSet

router = DefaultRouter()
router.register(r'games', GameViewSet, basename='game')
router.register(r'genres', GenreViewSet, basename='genre')

urlpatterns = [
    path('', include(router.urls)),
]
