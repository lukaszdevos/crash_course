from django.urls import include, path
from users import api_views

app_name = "users"


urlpatterns = [path("register/", api_views.UserCreateView.as_view())]
