from typing import List

from django.shortcuts import get_object_or_404
from ninja import Router

from .models import Product
from .schemas import ProductSchema

router = Router()


@router.get("/", response=List[ProductSchema])
def list_products(request):
    return Product.objects.all()


@router.get("/{product_id}", response=ProductSchema)
def get_product(request, product_id: int):
    return get_object_or_404(Product, id=product_id)
