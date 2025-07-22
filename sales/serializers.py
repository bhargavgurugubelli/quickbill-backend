from rest_framework import serializers
from .models import SalesInvoice, InvoiceItem
from .models import BusinessProfile



class BusinessProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessProfile
        fields = ['business_name', 'logo']

class InvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItem
        fields = ['item', 'quantity']

class SalesInvoiceSerializer(serializers.ModelSerializer):
    items = InvoiceItemSerializer(many=True)

    class Meta:
        model = SalesInvoice
        fields = ['id', 'customer_name', 'customer_phone', 'items', 'total_amount', 'created_at']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        invoice = SalesInvoice.objects.create(**validated_data)
        for item_data in items_data:
            InvoiceItem.objects.create(invoice=invoice, **item_data)
        return invoice
