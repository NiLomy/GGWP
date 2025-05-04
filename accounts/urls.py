from django.urls import path
from .views import RegisterView, LoginView, LogoutView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]

# from django.urls import path
# from .views import SignupAPIView, LoginAPIView, LogoutAPIView, HomeAPIView
#
# urlpatterns = [
#     path('signup/', SignupAPIView.as_view(), name='signup'),
#     path('login/', LoginAPIView.as_view(), name='login'),
#     path('home/', HomeAPIView.as_view(), name='home'),
# ]
