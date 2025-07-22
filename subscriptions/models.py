from django.db import models
from django.conf import settings  # Use settings.AUTH_USER_MODEL

class Subscriber(models.Model):
    mobile = models.CharField(max_length=15, unique=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.mobile

class Payment(models.Model):
    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE)
    plan_id = models.CharField(max_length=50)
    plan_name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=255, blank=True, null=True)

    payment_status = models.CharField(max_length=20)  # e.g. 'success', 'failed'
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.plan_name} - {self.subscriber.mobile} - {self.payment_status}"

