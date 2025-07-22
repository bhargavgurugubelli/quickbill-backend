from django.shortcuts import render
from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import SalesInvoiceSerializer
from .models import SalesInvoice, MenuItem
from django.db.models import Sum
from .models import BusinessProfile
from .serializers import BusinessProfileSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny  # ✅ Required for @permission_classes

import fitz  # PyMuPDF

# ✅ 1. Create Sales Invoice
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_invoice(request):
    serializer = SalesInvoiceSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        invoice = serializer.save()
        return Response({
            'status': 'success',
            'invoice_id': invoice.id,
            'order_id': invoice.order_id,
            'customer_name': invoice.customer_name,
            'total_amount': invoice.total_amount
        }, status=status.HTTP_201_CREATED)
    return Response({'status': 'error', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


# ✅ 2. Upload PDF Menu Items
@api_view(['POST'])
@parser_classes([MultiPartParser])
@permission_classes([AllowAny])
def upload_menu_pdf(request):
    pdf_file = request.FILES.get('pdf')

    if not pdf_file:
        return Response({"error": "No PDF uploaded"}, status=400)

    try:
        doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
        items = []

        for page in doc:
            text = page.get_text()
            for line in text.split('\n'):
                parts = line.rsplit(' ', 1)
                if len(parts) == 2 and parts[1].replace('.', '', 1).isdigit():
                    name, rate = parts
                    items.append(MenuItem(
                        business=request.user,
                        name=name.strip(),
                        rate=float(rate.strip())
                    ))

        MenuItem.objects.bulk_create(items, ignore_conflicts=True)
        return Response({"status": "success", "items_added": len(items)}, status=201)

    except Exception as e:
        return Response({"error": str(e)}, status=500)


# ✅ 3. Search Menu Items (for logged-in user)
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def search_menu_items(request):
    query = request.GET.get('q', '')
    items = MenuItem.objects.filter(
        business=request.user,
        name__icontains=query
    )[:10]

    data = [{'id': item.id, 'name': item.name, 'rate': item.rate} for item in items]
    return Response(data)


# ✅ 4. List Invoices (only for this user)
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def list_invoices(request):
    invoices = SalesInvoice.objects.filter(business=request.user).order_by('-created_at')
    serializer = SalesInvoiceSerializer(invoices, many=True)
    return Response(serializer.data)


# ✅ 5. Dashboard Summary (only for this user)
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def dashboard_summary(request):
    invoices = SalesInvoice.objects.filter(business=request.user)

    total_invoices = invoices.count()
    total_sales = invoices.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    latest_invoice = invoices.order_by('-created_at').first()
    pending_orders = invoices.filter(status='pending').count()

    return Response({
        'total_invoices': total_invoices,
        'total_sales': total_sales,
        'latest_order_id': latest_invoice.order_id if latest_invoice else None,
        'pending_orders': pending_orders,
    })

class BusinessProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        profile, created = BusinessProfile.objects.get_or_create(user=request.user)
        serializer = BusinessProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Profile saved successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def start_free_trial(request):
    user = request.user
    print("🎉 Trial started for:", user)
    return Response({"message": "Trial started"}, status=200)
