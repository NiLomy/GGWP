from rest_framework import viewsets, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Genre
from .serializers import GenreSerializer
from accounts.csrf import CsrfExemptSessionAuthentication

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .recommendation import get_recommended_game_ids
from .models import Game
from .serializers import GameSerializer


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


class GameRecommendationView(APIView):
    authentication_classes = (JWTAuthentication, CsrfExemptSessionAuthentication)
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            id1 = int(request.GET.get('id1'))
            id2 = int(request.GET.get('id2'))
        except (TypeError, ValueError):
            return Response({'error': 'Параметры id1 и id2 обязательны и должны быть целыми числами.'},
                            status=status.HTTP_400_BAD_REQUEST)

        recommended_ids = get_recommended_game_ids(id1, id2)
        games = Game.objects.filter(id__in=recommended_ids)
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)
