from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions, serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from users.models import ActivationToken, User


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
        user_token = ActivationToken.objects.create(user=user)
        print(user_token.token)  # TODO delete after CC-408


class UserLoginSerializer(TokenObtainPairSerializer):
    default_error_messages = {"no_active_account": _("Invalid username or password")}
