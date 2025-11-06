from __future__ import annotations

import logging

from django.conf import settings
from django.core.mail import send_mail

from pharmacy.celery import app

from .models import Sale

logger = logging.getLogger(__name__)


@app.task
def email_sale_receipt(sale_id: int) -> None:
    try:
        sale = Sale.objects.get(pk=sale_id)
    except Sale.DoesNotExist:
        logger.warning("Sale %s does not exist", sale_id)
        return

    if not sale.customer_email:
        logger.info("Sale %s has no customer email to send receipt.", sale.invoice_number)
        return

    subject = f"Receipt for Invoice {sale.invoice_number}"
    message = (
        f"Dear {sale.customer_name or 'Customer'},\n\n"
        f"Thank you for your purchase at {settings.SITE_NAME}.\n"
        f"Invoice: {sale.invoice_number}\n"
        f"Total amount: {sale.total}\n\n"
        "We appreciate your business.\n"
    )

    try:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [sale.customer_email])
    except Exception as exc:  # pragma: no cover - dependent on external service
        logger.error("Failed to send receipt for sale %s: %s", sale.invoice_number, exc)