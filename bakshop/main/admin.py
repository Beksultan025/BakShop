from django.contrib import admin
from .models import Product
from .models import Order


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "brand", "car", "price", "in_stock")
    list_filter = ("brand", "in_stock")
    search_fields = ("name", "brand", "car")
    list_editable = ("price", "in_stock")
    
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "product_name", "quantity", "name", "phone", "status", "created_at")
    list_filter = ("status",)
    list_editable = ("status",)
    search_fields = ("name", "phone", "product_name")