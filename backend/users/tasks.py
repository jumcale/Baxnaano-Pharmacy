from __future__ import annotations

from django.conf import settings
from django.core.mail import send_mail

from pharmacy.celery import app


@app.task
def send_welcome_email(user_email: str) -> None:
    if not user_email:
        return
    subject = f"Welcome to {settings.SITE_NAME}"
    message = (
        "Hello,\n\n"
        "Your Baxnaano Pharmacy account has been created successfully.\n"
        "You can now access the system and start managing the pharmacy operations.\n\n"
        "Best regards,\n"
        f"{settings.SITE_NAME} Team"
    )
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user_email])