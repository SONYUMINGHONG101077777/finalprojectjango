from django.contrib import admin
from .models import Product, Supplier, StockHistory

# -----------------------------
# Custom Admin with CSS
# -----------------------------
class CustomAdmin(admin.ModelAdmin):
    class Media:
        css = {
            'all': ('inventory/css/admin_custom.css',)  # path relative to static/
        }

# -----------------------------
# Supplier Admin
# -----------------------------
@admin.register(Supplier)
class SupplierAdmin(CustomAdmin):
    list_display = ('id', 'name', 'phone', 'email')
    search_fields = ('name', 'phone', 'email')

# -----------------------------
# Product Admin
# -----------------------------
@admin.register(Product)
class ProductAdmin(CustomAdmin):
    list_display = ('id', 'name', 'supplier', 'stock', 'minimum_stock', 'stock_status')
    search_fields = ('name', 'supplier__name')
    list_filter = ('supplier',)

    # Custom column to show stock status
    def stock_status(self, obj):
        return "Low Stock" if obj.stock < obj.minimum_stock else "OK"
    stock_status.short_description = "Stock Status"

# -----------------------------
# StockHistory Admin
# -----------------------------
@admin.register(StockHistory)
class StockHistoryAdmin(CustomAdmin):
    list_display = ('id', 'product', 'quantity', 'action_type', 'created_at')
    list_filter = ('action_type', 'created_at')
    search_fields = ('product__name',)
