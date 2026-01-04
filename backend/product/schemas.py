from decimal import Decimal
from typing import Any, Dict, List, Optional

from ninja import Schema


class ProductSchema(Schema):
    id: int
    name: str
    slug: str
    description: str
    price: Optional[Decimal] = None
    category: str
    type: str
    price_type: str
    rating: float
    reviews: int

    # JSON Fields
    features: List[str]
    specs: Dict[str, Any] = {}

    # Image List
    images: List[str]

    # Map 'specifications' from DB to 'specs' in Frontend
    @staticmethod
    def resolve_specs(obj):
        return obj.specifications

    # Extract URL strings from the related ProductImage model
    @staticmethod
    def resolve_images(obj):
        # This assumes you have configured MEDIA_URL in settings.py
        return [img.image.url for img in obj.images.all()]

    class Config:
        from_attributes = True
