from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers, exceptions
from rest_framework.settings import api_settings
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users.models import Activationtoken, User


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


class UserLoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        self._validate_login(attrs)
        return super().validate(attrs)

    def _validate_login(self, attrs):
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            'password': attrs['password'],
        }
        self.user = authenticate(**authenticate_kwargs)
        if self.user is None:
            raise exceptions.AuthenticationFailed("Invalid username or password")
