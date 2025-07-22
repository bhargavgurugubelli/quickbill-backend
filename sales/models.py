from django.db import models
from django.conf import settings

class BusinessProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    business_name = models.CharField(max_length=255, blank=True, null=True)

    logo = models.ImageField(upload_to='business_logos/', null=True, blank=True)

    def __str__(self):
        return self.business_name


class MenuItem(models.Model):
    business = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE, related_name='menu_items')
    name = models.CharField(max_length=100)
    rate = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class SalesInvoice(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('preparing', 'Preparing'),
        ('ready', 'Ready'),
        ('delivered', 'Delivered'),
    ]

    business = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE, related_name='invoices')
    customer_name = models.CharField(max_length=100)
    customer_phone = models.CharField(max_length=15)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    order_id = models.CharField(max_length=20, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.order_id:
            last_invoice = SalesInvoice.objects.filter(business=self.business).order_by('-id').first()
            last_id = int(last_invoice.order_id.split('-')[-1]) if last_invoice and last_invoice.order_id else 0
            self.order_id = f"ORD-{last_id + 1:05d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.order_id} - {self.customer_name} - ₹{self.total_amount}"


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(SalesInvoice, related_name='items', on_delete=models.CASCADE)
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.item.name} x {self.quantity} (Order {self.invoice.order_id})"
