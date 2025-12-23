from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'price_type')
    list_filter = ('price_type',)
    search_fields = ('name', 'description')