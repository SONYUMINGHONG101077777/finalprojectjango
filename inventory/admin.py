from django.contrib import admin
from .models import Product, Supplier, StockHistory

class CustomAdmin(admin.ModelAdmin):
    class Media:
        css = {
             'all': ('/static\inventory\css\ admin_custom.css',)
        }

@admin.register(Supplier)
class SupplierAdmin(CustomAdmin):
    list_display = ('id', 'name', 'phone', 'email')
    search_fields = ('name', 'phone', 'email')

@admin.register(Product)
class ProductAdmin(CustomAdmin):
    list_display = ('id', 'name', 'supplier', 'stock', 'minimum_stock')
    search_fields = ('name', 'supplier__name')
    list_filter = ('supplier',)

@admin.register(StockHistory)
class StockHistoryAdmin(CustomAdmin):
    list_display = ('id', 'product', 'quantity', 'action_type', 'created_at')
    list_filter = ('action_type', 'created_at')
    search_fields = ('product__name',)
