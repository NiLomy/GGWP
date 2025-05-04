from django.contrib.auth import authenticate
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegisterSerializer, LoginSerializer

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.validated_data)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Получаем refresh token из заголовка
            refresh_token = request.data.get('refresh')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()  # Добавляем в черный список
            return Response({"detail": "Successfully logged out."}, status=200)
        except Exception as e:
            return Response({"detail": str(e)}, status=400)
# from rest_framework import generics, permissions
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from django.contrib.auth import authenticate, login, logout
# from .serializers import UserSerializer
# from django.contrib.auth import get_user_model
# from accounts.csrf import CsrfExemptSessionAuthentication
# from rest_framework.permissions import IsAuthenticated
#
# User = get_user_model()
#
# class SignupAPIView(generics.CreateAPIView):
#     authentication_classes = (CsrfExemptSessionAuthentication,)
#     serializer_class = UserSerializer
#     permission_classes = [permissions.AllowAny]
#
# class LoginAPIView(APIView):
#     authentication_classes = (CsrfExemptSessionAuthentication,)
#     permission_classes = [permissions.AllowAny]
#
#     def post(self, request):
#         name = request.data.get('name')
#         password = request.data.get('password')
#         user = authenticate(request, username=name, password=password)
#         if user is not None:
#             login(request, user)
#             return Response({"detail": "Logged in successfully"})
#         return Response({"detail": "Invalid credentials"}, status=400)
#
# class LogoutAPIView(APIView):
#     authentication_classes = (CsrfExemptSessionAuthentication,)
#
#     def post(self, request):
#         logout(request)
#         return Response({"detail": "Logged out successfully"})
#
# class HomeAPIView(APIView):
#     authentication_classes = (CsrfExemptSessionAuthentication,)
#
#     def get(self, request):
#         print("User:", request.user, "Authenticated:", request.user.is_authenticated)
#         if not request.user.is_authenticated:
#             return Response({"detail": "Authentication required"}, status=401)
#         return Response({"message": f"Hello, {request.user.name}"})
#
# class ProtectedView(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request):
#         return Response({"message": "Это защищенный ресурс"})
