from rest_framework import viewsets, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Game
from .serializers import GameSerializer
from .models import Genre
from .serializers import GenreSerializer
from accounts.csrf import CsrfExemptSessionAuthentication

class GameViewSet(viewsets.ModelViewSet):
    authentication_classes = (JWTAuthentication, CsrfExemptSessionAuthentication)
    permission_classes = [permissions.IsAuthenticated]  # Проверка аутентификации
    queryset = Game.objects.all()
    serializer_class = GameSerializer

class GenreViewSet(viewsets.ModelViewSet):
    authentication_classes = (JWTAuthentication, CsrfExemptSessionAuthentication)
    permission_classes = [permissions.IsAuthenticated]  # Проверка аутентификации
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer