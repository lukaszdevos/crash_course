from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models


class User(AbstractBaseUser):
    email = models.EmailField(blank=False, unique=True)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
