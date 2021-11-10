import secrets

from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractBaseUser):
    email = models.EmailField(blank=False, unique=True)
    is_active = models.BooleanField(default=False)
    display_name = models.CharField(null=True, blank=True, max_length=128)

    USERNAME_FIELD = "email"


class UserToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.token = secrets.token_urlsafe()
        return super().save(*args, **kwargs)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserToken.objects.create(user=instance)
