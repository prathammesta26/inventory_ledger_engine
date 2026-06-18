# Admin configuration
from django.contrib import admin
from .models import InventoryItem, ReconciliationLog

# Register models to make them visible in the secure Django Admin Panel
admin.site.register(InventoryItem)
admin.site.register(ReconciliationLog)