from django.shortcuts import get_object_or_404, render

from .models import Product


# Create your views here.
def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    context = {"product": product}
    return render(request, "product_detail.html", context)
