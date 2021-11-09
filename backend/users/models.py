from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models


class User(AbstractBaseUser):
    email = models.EmailField(blank=False, unique=True)

    USERNAME_FIELD = "email"
