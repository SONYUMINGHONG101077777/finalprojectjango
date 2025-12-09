from django.db import models

# -----------------------------
# Supplier model
# -----------------------------
class Supplier(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.name

# -----------------------------
# Product model
# -----------------------------
class Product(models.Model):
    name = models.CharField(max_length=100)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True)
    stock = models.IntegerField(default=0)
    minimum_stock = models.IntegerField(default=10)

    def __str__(self):
        return self.name

# -----------------------------
# StockHistory model
# -----------------------------
class StockHistory(models.Model):
    IN = "IN"
    OUT = "OUT"
    ACTION_TYPE_CHOICES = [
        (IN, "Stock In"),
        (OUT, "Stock Out"),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    action_type = models.CharField(
        max_length=3,
        choices=ACTION_TYPE_CHOICES,
        default=IN  
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.action_type} - {self.quantity}"
