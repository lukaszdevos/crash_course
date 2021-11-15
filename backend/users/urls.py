from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users import api_views

app_name = "users"


urlpatterns = [
    path("register/", api_views.UserCreateView.as_view(), name="register"),
    path("activate/", api_views.UserActivateView.as_view(), name="activate"),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("login/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
