from django.conf import settings
from django.core.mail import send_mail

from .models import QuoteRequest


def send_quote_email_task(quote_id):
    try:
        quote = QuoteRequest.objects.get(id=quote_id)

        # 1. Email to Admin (You)
        admin_subject = f"New Quote Request: {quote.product.name}"
        admin_message = f"""
        New Lead!

        Product: {quote.product.name}
        Quantity: {quote.quantity}

        Customer: {quote.email}
        Phone: {quote.phone or "N/A"}
        User ID: {quote.user_id or "Guest"}

        Message:
        {quote.message}
        """

        send_mail(
            admin_subject,
            admin_message,
            settings.DEFAULT_FROM_EMAIL,
            [settings.DEFAULT_FROM_EMAIL],  # Send to yourself/admin
            fail_silently=False,
        )

        # 2. Confirmation Email to Customer
        customer_subject = f"We received your request: {quote.product.name}"
        customer_message = f"""
        Hi there,

        Thanks for requesting a quote for {quote.product.name} (Qty: {quote.quantity}).

        Our team has received your request and will get back to you shortly with pricing and availability.

        Best regards,
        The NexGen Team
        """

        send_mail(
            customer_subject,
            customer_message,
            settings.DEFAULT_FROM_EMAIL,
            [quote.email],
            fail_silently=True,
        )

    except QuoteRequest.DoesNotExist:
        print("Quote request not found")
