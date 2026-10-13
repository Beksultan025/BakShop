from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "brand", "car", "price", "in_stock")
    list_filter = ("brand", "in_stock")
    search_fields = ("name", "brand", "car")
    list_editable = ("price", "in_stock")