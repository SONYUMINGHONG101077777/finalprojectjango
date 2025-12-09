from rest_framework import serializers
from .models import Product, Supplier, StockHistory

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    supplier_name = serializers.CharField(source="supplier.name", read_only=True)

    class Meta:
        model = Product
        fields = "__all__"


class StockHistorySerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)

    class Meta:
        model = StockHistory
        fields = "__all__"


# -----------------------------
# Serializer for add/remove stock
# -----------------------------
class StockActionSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=1)
