# Bulk File Processing Logic
import time
import io
import csv
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import InventoryItem, ReconciliationLog

def dashboard_view(request):
    # Retrieve all saved item arrays and audit history logs
    items = InventoryItem.objects.all().order_by('sku')
    logs = ReconciliationLog.objects.all().order_by('-created_at')
    
    context = {
        'items': items,
        'logs': logs,
    }
    return render(request, 'ledger_dashboard.html', context)

def process_upload_view(request):
    if request.method != "POST":
        return redirect('ledger_dashboard')

    # Start system execution stopwatch
    start_time = time.time()
    
    # Extract the user-submitted text payload block from the web form
    raw_data = request.POST.get('bulk_data', '').strip()
    
    if not raw_data:
        messages.error(request, "Data submission stream cannot be empty.")
        return redirect('ledger_dashboard')

    try:
        # Use StringIO to handle raw string fields exactly like an uploaded file stream
        csv_file = io.StringIO(raw_data)
        reader = csv.reader(csv_file)
        
        # Extract the metadata header line: SKU, Product Name, Stock
        header = next(reader, None) 
        
        rows_processed = 0
        items_to_update = []
        items_to_create = []
        
        # Pull existing records into a Python dictionary map to allow algorithmic O(1) runtime comparisons
        existing_items = {item.sku: item for item in InventoryItem.objects.all()}

        for row in reader:
            if len(row) < 3:
                continue # Gracefully skip empty or broken lines
                
            sku, name, stock_str = row[0].strip(), row[1].strip(), row[2].strip()
            new_stock = int(stock_str)
            rows_processed += 1

            if sku in existing_items:
                # Update existing records inside the local local system memory array
                item = existing_items[sku]
                item.product_name = name
                item.warehouse_stock = new_stock
                items_to_update.append(item)
            else:
                # Prepare a completely fresh database entity record tracking array
                new_item = InventoryItem(sku=sku, product_name=name, warehouse_stock=new_stock)
                items_to_create.append(new_item)

        # ENGINE BULK OPTIMIZATION: Push data changes to the database in single queries
        if items_to_create:
            InventoryItem.objects.bulk_create(items_to_create)
        if items_to_update:
            InventoryItem.objects.bulk_update(items_to_update, ['product_name', 'warehouse_stock'])

        # Calculate execution latency metrics
        end_time = time.time()
        duration_ms = (end_time - start_time) * 1000

        # Log processing status inside our immutable execution log model
        ReconciliationLog.objects.create(
            filename="bulk_stream_payload.csv",
            rows_processed=rows_processed,
            status="SUCCESS",
            execution_time_ms=round(duration_ms, 2)
        )
        
        messages.success(request, f"Successfully processed {rows_processed} lines using optimized bulk matrix queues!")

    except Exception as e:
        end_time = time.time()
        duration_ms = (end_time - start_time) * 1000
        ReconciliationLog.objects.create(
            filename="bulk_stream_payload.csv",
            rows_processed=0,
            status=f"FAILED: {str(e)}",
            execution_time_ms=round(duration_ms, 2)
        )
        messages.error(request, f"Relational engine exception: {str(e)}")

    return redirect('ledger_dashboard')