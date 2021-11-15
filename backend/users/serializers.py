from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import exceptions, serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from handlers import send_registration_confirmation_mail
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
        user_token = self._create_user_token(user)
        self._send_activation_mail(user, user_token)
        return user

    def _create_user_token(self, user):
        return Activationtoken.objects.create(user=user)

    def _send_activation_mail(self, user, user_token):
        url_token = self._get_activation_url(user_token)
        send_registration_confirmation_mail(url_token, user.email)

    def _get_activation_url(self, user_token):
        token = user_token.token
        request = self.context.get("request")
        return request.build_absolute_uri("/users/activate?token=" + token)


class UserLoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        self._validate_login(attrs)
        return super().validate(attrs)

    def _validate_login(self, attrs):
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            "password": attrs["password"],
        }
        self.user = authenticate(**authenticate_kwargs)
        if self.user is None:
            raise exceptions.AuthenticationFailed("Invalid username or password")
