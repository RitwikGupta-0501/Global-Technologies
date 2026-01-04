from ninja import Schema


# --- Schemas ---
class QuoteInputSchema(Schema):
    product_id: int
    email: str
    phone: str = ""
    quantity: int = 1
    message: str = ""


class QuoteSuccessSchema(Schema):
    message: str
    quote_id: int


#
