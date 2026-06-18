# Inventory & Audit Ledger Tables
from django.db import models

class InventoryItem(models.Model):
    sku = models.CharField(max_length=50, unique=True)
    product_name = models.CharField(max_length=255)
    warehouse_stock = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.sku} - {self.product_name} ({self.warehouse_stock} units)"

class ReconciliationLog(models.Model):
    filename = models.CharField(max_length=255)
    rows_processed = models.IntegerField()
    status = models.CharField(max_length=50, default="SUCCESS")
    execution_time_ms = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"File: {self.filename} | Status: {self.status}"