import datetime

from celery import shared_task
from celery.utils.log import get_task_logger
from django.utils import timezone
from handlers import send_task_notifiaction_mail
from projects.models import Task

logger = get_task_logger(__name__)


@shared_task
def notifiaction_task():
    tasks = Task.objects.all()
    for task in tasks:
        task_url = (
            "localhost:8000" + "/project/" + str(task.project.id) + "/tasks/" + str(task.id)
        )
        if task.due_date and task.status != Task.DONE:
            if task.due_date + datetime.timedelta(hours=1) > timezone.now():
                send_task_notifiaction_mail(task.title, task_url, task.member.email)
