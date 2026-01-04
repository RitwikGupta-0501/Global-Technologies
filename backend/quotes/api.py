from django.shortcuts import get_object_or_404
from django_q.tasks import async_task
from ninja import Router
from ninja_jwt.authentication import JWTAuth
from product.models import Product

from .models import QuoteRequest
from .schemas import QuoteInputSchema, QuoteSuccessSchema

router = Router()


# --- Endpoints ---
@router.post("/request", response=QuoteSuccessSchema, auth=JWTAuth())
def create_quote_request(request, data: QuoteInputSchema):
    # 1. Validate Product exists
    product = get_object_or_404(Product, id=data.product_id)

    # 2. Create Database Entry
    quote = QuoteRequest.objects.create(
        product=product,
        user=request.auth
        if request.auth
        else None,  # If you use auth=JWTAuth() optionally
        email=data.email,
        phone=data.phone,
        quantity=data.quantity,
        message=data.message,
    )

    # 3. Offload Email Task
    async_task("quotes.tasks.send_quote_email_task", quote.id)

    return {"message": "Quote request received successfully", "quote_id": quote.id}
