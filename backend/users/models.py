from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models


class User(AbstractBaseUser):
    email = models.EmailField(blank=False, unique=True)
    is_active = models.BooleanField(default=False)
    display_name = models.CharField(null=True, blank=True, max_length=128)

    USERNAME_FIELD = "email"


class UserToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE())
    token = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)

