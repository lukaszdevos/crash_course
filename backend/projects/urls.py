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
    # "delete": "destroy",
}

METHOD_DETIAL_WITH_DELETE = {
    "get": "retrieve",
    "put": "update",
    "patch": "partial_update",
    "delete": "destroy",
}

project_list = api_views.ProjectViewSet.as_view(METHOD_LIST)
project_detail = api_views.ProjectViewSet.as_view(METHOD_DETIAL)
task_list = api_views.TaskViewSet.as_view(METHOD_LIST)
task_detail = api_views.TaskViewSet.as_view(METHOD_DETIAL_WITH_DELETE)

app_name = "projects"

urlpatterns = [
    path("", project_list, name="project-list"),
    path("<int:pk>/", project_detail, name="project-detail"),
    path("<int:pk>/tasks/", task_list, name="task-list")
]
