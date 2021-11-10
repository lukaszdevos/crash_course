from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = [
            "email",
            "password",
        ]

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data.get("password"))
        user.save()
        return user
