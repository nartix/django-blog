from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_email_task(subject, message, recipient_list, sender_name="Feroz Faiz"):
    send_mail(
        subject,
        message,
        f"{sender_name} <{settings.EMAIL_SENDER_ADDRESS}>",  # Sender email
        recipient_list,  # List of recipients
        fail_silently=False,
    )


@shared_task
def hello_world():
    return "Hello World"
