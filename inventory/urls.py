from django.urls import path, include
from rest_framework import routers
from django.http import JsonResponse

from .views import ProductViewSet, SupplierViewSet, StockHistoryViewSet

router = routers.DefaultRouter()
router.register("products", ProductViewSet)
router.register("suppliers", SupplierViewSet)
router.register("stock-history", StockHistoryViewSet)


def api_home(request):
    return JsonResponse({
        "message": "Inventory API",
        "endpoints": {
            "products": "/api/products/",
            "suppliers": "/api/suppliers/",
            "stock_history": "/api/stock-history/"
        }
    })


urlpatterns = [
    path('', api_home),       
    path('', include(router.urls)),
]
