from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from django.core.mail import send_mail
import threading

from .models import Product, Supplier, StockHistory
from .serializers import ProductSerializer, SupplierSerializer, StockHistorySerializer, StockActionSerializer

class ProductViewSet(viewsets.ModelViewSet):
    """CRUD + Stock management"""
    
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # ----- ADD STOCK -----
    @action(detail=True, methods=["POST"])
    def add_stock(self, request, pk=None):
        product = self.get_object()
        serializer = StockActionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        quantity = serializer.validated_data['quantity']

        with transaction.atomic():
            product.stock += quantity
            product.save()
            StockHistory.objects.create(product=product, quantity=quantity, action_type="IN")

        return Response({
            "message": "Stock added successfully",
            "product": product.name,
            "new_stock": product.stock
        }, status=status.HTTP_200_OK)

    # ----- REMOVE STOCK -----
    @action(detail=True, methods=["POST"])
    def remove_stock(self, request, pk=None):
        product = self.get_object()
        serializer = StockActionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        quantity = serializer.validated_data['quantity']

        if quantity > product.stock:
            return Response({"error": "Not enough stock"}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            product.stock -= quantity
            product.save()
            StockHistory.objects.create(product=product, quantity=quantity, action_type="OUT")

        # ----- Send low stock alert asynchronously -----
        if product.stock < product.minimum_stock:
            threading.Thread(target=send_mail, kwargs={
                "subject": "Low Stock Alert",
                "message": f"Product: {product.name} is low. Remaining: {product.stock}",
                "from_email": "admin@example.com",
                "recipient_list": ["owner@example.com"],
                "fail_silently": True,
            }).start()

        return Response({
            "message": "Stock removed",
            "product": product.name,
            "new_stock": product.stock
        }, status=status.HTTP_200_OK)


# -------- Supplier View ---------
class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer


# -------- Stock History View ---------
class StockHistoryViewSet(viewsets.ModelViewSet):
    queryset = StockHistory.objects.all()
    serializer_class = StockHistorySerializer
