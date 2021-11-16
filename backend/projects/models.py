from django.core.validators import MaxLengthValidator
from django.db import models
from users.models import User


class Project(models.Model):
    name = models.CharField(max_length=128, blank=False)
    member = models.ManyToManyField(User, blank=True, related_name="project")
    created_by = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, related_name="created_by"
    )
    created_at = models.DateTimeField(auto_now_add=True)


class Task(models.Model):
    TO_DO = "TO DO"
    IN_PROGRESS = "IN PROGRESS"
    REVIEW = "REVIEW"
    DONE = "DONE"
    STATUS_CHOICES = (
        (TO_DO, "TO DO"),
        (IN_PROGRESS, "IN PROGRESS"),
        (REVIEW, "REVIEW"),
        (DONE, "DONE_"),
    )

    title = models.CharField(max_length=128, blank=False)
    description = models.TextField(validators=[MaxLengthValidator(10000)])
    status = models.CharField(max_length=32, choices=STATUS_CHOICES)
    member = models.OneToOneField(User, on_delete=models.DO_NOTHING, blank=True)
    due_date = models.DateTimeField(blank=True)
    created_by = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, related_name="created_by"
    )
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    edited_at = models.DateTimeField(auto_now_add=True)
