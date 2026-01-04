from django.conf import settings
from django.db import models


class QuoteRequest(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("CONTACTED", "Contacted"),
        ("CLOSED", "Closed"),
    ]

    # Link to user if they are logged in (optional)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    # Link to the product they want
    product = models.ForeignKey(
        "product.Product",  # Assuming your product app is named 'product'
        on_delete=models.CASCADE,
        related_name="quote_requests",
    )

    # Contact Info
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)

    # Request Details
    quantity = models.PositiveIntegerField(default=1)
    message = models.TextField(blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Quote: {self.email} - {self.product.name}"
