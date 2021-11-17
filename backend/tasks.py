from datetime import datetime

from celery import shared_task
from celery.utils.log import get_task_logger
from django.utils import timezone
from projects.models import Task

logger = get_task_logger(__name__)


@shared_task
def sample_task():
    logger.info("sample CELERY")
    tasks = Task.objects.all()
    for task in tasks:
        if task.due_date:
            if task.due_date + datetime.timedelta(hours=1) > timezone.now():
                # send mail
                pass
