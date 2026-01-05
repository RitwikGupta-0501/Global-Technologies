from typing import List

import razorpay
from django.conf import settings
from django.db import transaction
from django.shortcuts import get_object_or_404
from ninja import Router
from product.models import Product

from .models import Order, OrderItem, SavedAddress
from .schemas import OrderCreateSchema, OrderInitSchema, SavedAddressSchema

router = Router()

# Initialize Razorpay Client
client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


# --- ENDPOINTS ---
@router.post("/initiate", response=OrderInitSchema, auth=None)
def initiate_order(request, data: OrderCreateSchema):
    with transaction.atomic():
        # 1. Create the Local Order Record
        order = Order.objects.create(
            user=request.auth if request.auth else None,
            first_name=data.first_name,
            last_name=data.last_name,
            email=data.email,
            phone=data.phone,
            company_name=data.company_name,
            gstin=data.gstin,
            # Billing
            billing_address_line1=data.billing_address.address_line1,
            billing_address_line2=data.billing_address.address_line2,
            billing_city=data.billing_address.city,
            billing_state=data.billing_address.state,
            billing_pincode=data.billing_address.pincode,
            # Shipping
            shipping_address_line1=data.shipping_address.address_line1,
            shipping_address_line2=data.shipping_address.address_line2,
            shipping_city=data.shipping_address.city,
            shipping_state=data.shipping_address.state,
            shipping_pincode=data.shipping_address.pincode,
            status="PENDING",
        )

        # 2. Process Items & Calculate Total
        if data.save_info and request.auth:
            # Save Shipping
            SavedAddress.objects.create(
                user=request.auth,
                type="SHIPPING",
                full_name=f"{data.first_name} {data.last_name}",
                phone=data.phone,
                address_line1=data.shipping_address.address_line1,
                address_line2=data.shipping_address.address_line2,
                city=data.shipping_address.city,
                state=data.shipping_address.state,
                pincode=data.shipping_address.pincode,
            )

        calculated_total = 0
        for item_data in data.items:
            product = get_object_or_404(Product, id=item_data.product_id)

            if product.price_type != "fixed" or not product.price:
                continue  # Skip quote items

            line_total = product.price * item_data.quantity
            calculated_total += line_total

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item_data.quantity,
                price_at_purchase=product.price,
            )

        order.total_amount = calculated_total
        order.save()

        # 3. Create Razorpay Order
        # Razorpay expects amount in PAISE (multiply by 100)
        amount_in_paise = int(calculated_total * 100)

        razorpay_order_data = {
            "amount": amount_in_paise,
            "currency": "INR",
            "receipt": f"order_rcptid_{order.id}",
            "payment_capture": 1,  # Auto capture
        }

        razorpay_order = client.order.create(data=razorpay_order_data)

        # 4. Save Razorpay ID to DB
        order.razorpay_order_id = razorpay_order["id"]
        order.save()

    return {
        "order_id": order.id,
        "razorpay_order_id": order.razorpay_order_id,
        "amount": calculated_total,
        "currency": "INR",
        "key_id": settings.RAZORPAY_KEY_ID,
    }


@router.get("/my-addresses", response=List[SavedAddressSchema])
def get_my_addresses(request):
    # This requires the user to be logged in
    if not request.auth:
        return []
    return SavedAddress.objects.filter(user=request.auth)
