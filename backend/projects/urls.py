from django.urls import path
from projects import api_views

METHOD_LIST = {
    "get": "list",
    "post": "create",
}

METHOD_DETIAL = {
    "get": "retrieve",
    "put": "update",
    "patch": "partial_update",
}

project_list = api_views.ProjectViewSet.as_view(METHOD_LIST)
project_detail = api_views.ProjectViewSet.as_view(METHOD_DETIAL)
task_list = api_views.TaskViewSet.as_view(METHOD_LIST)
task_detail = api_views.TaskViewSet.as_view(METHOD_DETIAL)

app_name = "projects"

urlpatterns = [
    path("", project_list, name="project-list"),
    path("<int:pk>/", project_detail, name="project-detail"),
    path("<int:project_pk>/tasks/", task_list, name="task-list"),
    path("<int:project_pk>/tasks/<int:pk>/", task_detail, name="task-detail"),
]
