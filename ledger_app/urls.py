# App-specific routing routes
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='ledger_dashboard'),
    path('process-upload/', views.process_upload_view, name='process_upload'),
]