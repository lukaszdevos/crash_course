from django.urls import include, path
from projects import api_views
from rest_framework import routers

router = routers.DefaultRouter()
router.register("", api_views.ProjectViewSet, basename="project")

app_name = "projects"

urlpatterns = [
    path("", include(router.urls)),
]
