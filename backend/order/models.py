from django.conf import settings
from django.db import models
from product.models import Product


# Create your models here.
class SavedAddress(models.Model):
    ADDRESS_TYPE_CHOICES = [
        ("BILLING", "Billing"),
        ("SHIPPING", "Shipping"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="saved_addresses",
        on_delete=models.CASCADE,
    )
    type = models.CharField(
        max_length=10, choices=ADDRESS_TYPE_CHOICES, default="SHIPPING"
    )

    # Common Fields
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)

    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.email} - {self.city} ({self.type})"


class Order(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Pending Payment"),
        ("PAID", "Paid"),
        ("FAILED", "Failed"),
        ("SHIPPED", "Shipped"),
        ("COMPLETED", "Completed"),
    ]

    # --- 1. Customer Identity ---
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)

    # --- 2. Business Info (Optional) ---
    company_name = models.CharField(max_length=255, blank=True, null=True)
    gstin = models.CharField(max_length=20, blank=True, null=True)

    # --- 3. Billing Address ---
    billing_address_line1 = models.CharField(max_length=255)
    billing_address_line2 = models.CharField(max_length=255, blank=True)
    billing_city = models.CharField(max_length=100)
    billing_state = models.CharField(max_length=100)
    billing_pincode = models.CharField(max_length=10)

    # --- 4. Shipping Address ---
    shipping_address_line1 = models.CharField(max_length=255)
    shipping_address_line2 = models.CharField(max_length=255, blank=True)
    shipping_city = models.CharField(max_length=100)
    shipping_state = models.CharField(max_length=100)
    shipping_pincode = models.CharField(max_length=10)

    # --- 5. Financials ---
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")

    # --- 6. Razorpay Specifics ---
    razorpay_order_id = models.CharField(
        max_length=100, unique=True, blank=True, null=True
    )
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_signature = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} - {self.first_name} {self.last_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)

    quantity = models.PositiveIntegerField(default=1)
    price_at_purchase = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.quantity}x {self.product.name}"
