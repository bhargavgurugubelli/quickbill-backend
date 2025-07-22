from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, mobile, password=None, **extra_fields):
        if not mobile:
            raise ValueError('Mobile number is required')
        user = self.model(mobile=mobile, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, mobile, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(mobile, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    mobile = models.CharField(max_length=15, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    is_trial = models.BooleanField(default=True)
    trial_expires_at = models.DateTimeField(null=True, blank=True)

    is_paid = models.BooleanField(default=False)  # ✅ Newly added field

    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'mobile'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.mobile
