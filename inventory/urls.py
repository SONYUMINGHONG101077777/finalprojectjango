from django.urls import path, include
from rest_framework import routers
from . import views

# DRF router
router = routers.DefaultRouter()
router.register(r'products', views.ProductViewSet)
router.register(r'suppliers', views.SupplierViewSet)
router.register(r'stockhistory', views.StockHistoryViewSet)

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),  # traditional dashboard view
    path('api/', include(router.urls)),                     # DRF API endpoints
]
