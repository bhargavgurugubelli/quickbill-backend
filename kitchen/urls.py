from django.urls import path
from .views import kitchen_orders, update_order_status

urlpatterns = [
    path('orders/', kitchen_orders, name='kitchen-orders'),
    path('orders/<int:invoice_id>/status/', update_order_status, name='update-order-status'),
]
