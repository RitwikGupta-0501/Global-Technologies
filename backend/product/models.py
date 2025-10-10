from django.db import models

class Product(models.Model):
    class PriceTypes(models.TextChoices):
        FIXED = 'F'
        NEGOTIABLE = 'N'

    name: str = models.CharField(verbose_name="Product Name")
    description: str = models.TextField(verbose_name="Product Description")
    price: float = models.FloatField(verbose_name="Product Price")
    price_type: str = models.CharField(max_length=1, choices=PriceTypes, verbose_name="Price Type")
    
    # TODO: Add More Fields later as per requirement
