from crashcourse.settings import FRONTEND_URL
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from handlers import send_registration_confirmation_mail
from rest_framework import serializers
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
        user_token = self._create_user_token(user)
        self._send_activation_mail(user, user_token)
        return user

    def _create_user_token(self, user):
        return ActivationToken.objects.create(user=user)

    def _send_activation_mail(self, user, user_token):
        url_token = self._get_activation_url(user_token)
        send_registration_confirmation_mail(url_token, user.email)

    def _get_activation_url(self, user_token):
        token = user_token.token
        return FRONTEND_URL + "/login/?token=" + token


class UserLoginSerializer(TokenObtainPairSerializer):
    default_error_messages = {"no_active_account": _("Invalid username or password")}


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "display_name"]
