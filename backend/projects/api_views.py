from projects.models import Project
from projects.serializers import ProjectSerializer
from rest_framework.viewsets import ModelViewSet


class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
