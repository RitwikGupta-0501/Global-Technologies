from django.shortcuts import render
from product.models import Product

# Create your views here.
def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    context = {
        'product': product
    }
    return render(request, 'product_detail.html', context)