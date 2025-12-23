from django.db import models


class Product(models.Model):
    class PriceTypes(models.TextChoices):
        FIXED = "F", "Fixed"
        NEGOTIABLE = "N", "Negotiable"

    name = models.CharField(max_length=255, verbose_name="Product Name")
    description = models.TextField(verbose_name="Product Description")
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Product Price",
        null=True,
        blank=True,
    )
    price_type = models.CharField(
        max_length=1,
        choices=PriceTypes.choices,
        default=PriceTypes.FIXED,
        verbose_name="Price Type",
    )
    image = models.ImageField(
        upload_to="products/", verbose_name="Product Image", null=True, blank=True
    )

    def __str__(self):
        return self.name

    # TODO: Add More Fields later as per requirement
