from projects.models import Project, Task
from rest_framework import serializers


class ProjectBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "name", "member"]

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["created_by_id"] = user.id
        return super().create(validated_data)


class ProjectExtendSerializer(ProjectBasicSerializer):
    class Meta(ProjectBasicSerializer.Meta):
        fields = ["name", "member", "created_by", "created_at"]


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["id", "title", "description", "status", "member", "due_date"]

    def create(self, validated_data):
        user = self.context["request"].user
        project_id = self.context["view"].kwargs.get("project_pk")
        validated_data["created_by_id"] = user.id
        validated_data["project_id"] = project_id
        return super().create(validated_data)
