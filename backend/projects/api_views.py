from django.db.models import Q
from projects.models import Project
from projects.serializers import (ProjectBasicSerializer,
                                  ProjectExtendSerializer)
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet


class ProjectViewSet(
    mixins.UpdateModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = Project.objects.all()
    serializer_class = ProjectBasicSerializer

    def get_queryset(self):
        return self.queryset.filter(
            Q(created_by=self.request.user) | Q(member=self.request.user.id)
        )

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ProjectExtendSerializer
        return self.serializer_class
