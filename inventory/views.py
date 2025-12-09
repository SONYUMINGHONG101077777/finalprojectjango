from django.shortcuts import render, redirect
from django.db import transaction
from django.core.mail import send_mail
from .models import Product, Supplier, StockHistory

# -----------------------------
# Traditional Dashboard View
# -----------------------------
def dashboard(request):
    suppliers = Supplier.objects.all()

    if request.method == "POST":
        name = request.POST.get("name")
        supplier_id = request.POST.get("supplier")
        stock = int(request.POST.get("stock") or 0)
        minimum_stock = int(request.POST.get("minimum_stock") or 10)

        with transaction.atomic():
            Product.objects.create(
                name=name,
                supplier_id=supplier_id,
                stock=stock,
                minimum_stock=minimum_stock
            )

        return redirect('dashboard')

    product_names = list(Product.objects.values_list("name", flat=True))
    product_stocks = list(Product.objects.values_list("stock", flat=True))

    context = {
        "suppliers": suppliers,
        "product_names": product_names,
        "product_stocks": product_stocks,
    }
    return render(request, "dashboard.html", context)


# -----------------------------
# DRF API ViewSets
# -----------------------------
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
import threading
from .serializers import ProductSerializer, SupplierSerializer, StockHistorySerializer, StockActionSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(detail=True, methods=["POST"])
    def add_stock(self, request, pk=None):
        product = self.get_object()
        serializer = StockActionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        quantity = serializer.validated_data["quantity"]

        with transaction.atomic():
            product.stock += quantity
            product.save()
            StockHistory.objects.create(product=product, quantity=quantity, action_type="IN")

        return Response({
            "message": "Stock added successfully",
            "product": product.name,
            "new_stock": product.stock
        })

    @action(detail=True, methods=["POST"])
    def remove_stock(self, request, pk=None):
        product = self.get_object()
        serializer = StockActionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        quantity = serializer.validated_data["quantity"]

        if quantity > product.stock:
            return Response({"error": "Not enough stock"}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            product.stock -= quantity
            product.save()
            StockHistory.objects.create(product=product, quantity=quantity, action_type="OUT")

        # Low stock email alert
        if product.stock < product.minimum_stock:
            threading.Thread(
                target=lambda: send_mail(
                    "Low Stock Alert",
                    f"Product {product.name} is low (stock: {product.stock})",
                    "admin@example.com",
                    ["owner@example.com"]
                ),
                daemon=True
            ).start()

        return Response({
            "message": "Stock removed successfully",
            "product": product.name,
            "new_stock": product.stock
        })


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer


class StockHistoryViewSet(viewsets.ModelViewSet):
    queryset = StockHistory.objects.all()
    serializer_class = StockHistorySerializer
