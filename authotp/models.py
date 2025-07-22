from django.db import models
from django.utils import timezone
from datetime import timedelta

class OTPStorage(models.Model):
    mobile = models.CharField(max_length=15)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_otp_expired(self):
        """Check if OTP is older than 5 minutes."""
        return timezone.now() > self.created_at + timedelta(minutes=5)

    def __str__(self):
        return f"{self.mobile} - {self.otp}"
