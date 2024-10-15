from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import CreateAccountView, LoginView, LogoutView, ChangePasswordView, refresh_token_view


app_name = 'logements'
urlpatterns = [
]
