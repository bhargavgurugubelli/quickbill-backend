from django.urls import path
from .views import BusinessProfileView
from .views import (
    create_invoice,
    upload_menu_pdf,
    search_menu_items,
    list_invoices,
    dashboard_summary,
    start_free_trial,  # ✅ fixed spelling and comma
)

urlpatterns = [
    path('create-invoice/', create_invoice, name='create-invoice'),
    path('upload-menu/', upload_menu_pdf, name='upload-menu'),
    path('search-items/', search_menu_items, name='search-items'),
    path('list-invoices/', list_invoices, name='list-invoices'),
    path('summary/', dashboard_summary, name='dashboard-summary'),
    path('api/business-profile/', BusinessProfileView.as_view(), name='business-profile'),
    path('api/start-free-trial/', start_free_trial, name='start-free-trial'),  # ✅ corrected spelling
]
