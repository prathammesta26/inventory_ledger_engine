# Project URLs placeholder
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.split('/')[0] if hasattr(admin.site, 'split') else admin.site.urls),
    path('', include('ledger_app.urls')),  # Connects your app to the main website domain
]