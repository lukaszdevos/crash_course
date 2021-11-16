from projects.models import Project
from rest_framework import serializers


class ProjectBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["name", "member"]

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["created_by_id"] = user.id
        return super().create(validated_data)


class ProjectExtendSerializer(ProjectBasicSerializer):
    class Meta(ProjectBasicSerializer.Meta):
        fields = ["name", "member", "created_by", "created_at"]
