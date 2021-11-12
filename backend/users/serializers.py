from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from users.models import User, Activationtoken


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )

    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "display_name",
        ]

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data["password"])
        user.save()
        self._create_user_token(user)
        return user

    def _create_user_token(self, user):
        user_token = Activationtoken.objects.create(user=user)
        print(user_token.token)  # TODO delete after CC-408
