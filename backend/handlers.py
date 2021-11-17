from crashcourse.settings import FROM_EMAIL
from django.core.mail import send_mail


def send_registration_confirmation_mail(url_token, user_mail):
    send_mail(
        subject="Crash Course - Please activate your account",
        message="Follow this link to activate your account: {}".format(url_token),
        from_email=FROM_EMAIL,
        recipient_list=[user_mail],
    )


def send_task_notifiaction_mail(title, task_url, user_email):
    send_mail(
        subject="Crash Course - Your task {} is about to exceed the deadline.".format(
            title
        ),
        message="Follow this link to see the task: {}".format(task_url),
        from_email=FROM_EMAIL,
        recipient_list=[user_email],
    )
