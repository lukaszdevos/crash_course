import datetime
import secrets

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager
from django.db import models
from django.utils import timezone
from exceptions import TokenException


class User(AbstractBaseUser):
    email = models.EmailField(blank=False, unique=True)
    is_active = models.BooleanField(default=False)
    display_name = models.CharField(null=True, blank=True, max_length=128)

    objects = UserManager()
    USERNAME_FIELD = "email"


class ActivationTokenManager(models.Manager):
    def activate(self, token):
        user_token = super().get_queryset().filter(token=token).first()
        if not user_token:
            raise TokenException("Token verification is invalid.")
        if not user_token.is_valid_token():
            raise TokenException("Token verification expired.")
        User.objects.filter(id=user_token.user.id).update(is_active=True)


class ActivationToken(models.Model):
    HOURS_TO_EXPIRED = 24

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="token")
    token = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = ActivationTokenManager()

    def save(self, *args, **kwargs):
        self.token = secrets.token_urlsafe()
        return super().save(*args, **kwargs)

    def is_valid_token(self):
        return timezone.now() <= self._get_expiration_time()

    def _get_expiration_time(self):
        return self.created_at + datetime.timedelta(hours=self.HOURS_TO_EXPIRED)
