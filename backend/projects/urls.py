from django.urls import path, include
from rest_framework import routers
from projects import api_views

router = routers.DefaultRouter()
router.register("", api_views.ProjectViewSet, basename="project")

app_name = "projects"

urlpatterns = [
    path("", include(router.urls)),
]
