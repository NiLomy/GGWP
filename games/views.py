from rest_framework import viewsets
from .models import Game
from .serializers import GameSerializer
from .models import Genre
from .serializers import GenreSerializer
from accounts.csrf import CsrfExemptSessionAuthentication

class GameViewSet(viewsets.ModelViewSet):
    authentication_classes = (CsrfExemptSessionAuthentication,)
    queryset = Game.objects.all()
    serializer_class = GameSerializer

class GenreViewSet(viewsets.ModelViewSet):
    authentication_classes = (CsrfExemptSessionAuthentication,)
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer