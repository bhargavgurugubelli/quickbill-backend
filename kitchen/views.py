from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from sales.models import SalesInvoice
from sales.serializers import SalesInvoiceSerializer

# ✅ 1. View all active kitchen orders
@api_view(['GET'])
# @permission_classes([IsAuthenticated])  # 👈 Uncomment this in production
def kitchen_orders(request):
    try:
        # Temporary logic: allow access even without login (for testing)
        if request.user.is_authenticated:
            orders = SalesInvoice.objects.filter(business=request.user).order_by('-created_at')
        else:
            # Show latest 10 invoices in dev mode
            orders = SalesInvoice.objects.all().order_by('-created_at')[:10]

        serializer = SalesInvoiceSerializer(orders, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({"error": str(e)}, status=500)

# ✅ 2. Update the order status
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_order_status(request, invoice_id):
    try:
        invoice = SalesInvoice.objects.get(id=invoice_id, business=request.user)
    except SalesInvoice.DoesNotExist:
        return Response({"error": "Invoice not found"}, status=404)

    new_status = request.data.get('status')

    if new_status not in ['Pending', 'Preparing', 'Ready']:
        return Response({"error": "Invalid status"}, status=400)

    invoice.status = new_status
    invoice.save()

    # OPTIONAL: Trigger WhatsApp message here based on new_status
    # Example: send_whatsapp_message(invoice.customer_phone, message)

    return Response({"success": True, "status": invoice.status}, status=200)
