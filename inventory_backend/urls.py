from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render

# simple home view
def home(request):
    return render(request, 'home.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('', include('inventory.urls')),  # include app-level urls
]
