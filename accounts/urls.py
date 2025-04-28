from django.urls import path
from .views import SignupAPIView, LoginAPIView, LogoutAPIView, HomeAPIView

urlpatterns = [
    path('signup/', SignupAPIView.as_view(), name='signup'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('home/', HomeAPIView.as_view(), name='home'),
]
