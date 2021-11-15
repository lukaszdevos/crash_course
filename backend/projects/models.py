from django.db import models

from users.models import User


class Project(models.Model):
    name = models.CharField(max_length=128, blank=False)
    member = models.ManyToManyField(User, blank=True, related_name="project")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_by")
