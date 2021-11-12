from django.urls import path
from users import api_views

app_name = "users"


urlpatterns = [
    path("register/", api_views.UserCreateView.as_view(), name="register"),
    path("login/", api_views.UserLoginView.as_view(), name="login"),
]
