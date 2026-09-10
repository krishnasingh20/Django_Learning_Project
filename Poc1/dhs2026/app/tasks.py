from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from.services import (
    get_message1,
    get_message2,
    get_html1,
    get_html2,
)


@shared_task
def send_workshop_email(email):
    send_mail(
        subject="DataHack Summit 2026 Workshops Inside.",
        message=get_message1(),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
        html_message=get_html1(),
    )


@shared_task
def send_agenda_email(email):
    send_mail(
        subject="Your Agenda for DataHack Summit 2026",
        message=get_message2(),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        html_message=get_html2()
    )