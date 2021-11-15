from django.core.mail import send_mail

from crashcourse.settings import FROM_EMAIL


def send_registration_confirmation_mail(url_token, user_mail):
    send_mail(
        subject="Crash Course - Please activate your account",
        message="Follow this link to activate your account: {}".format(url_token),
        from_email=FROM_EMAIL,
        recipient_list=[user_mail]
    )
