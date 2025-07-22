from django.urls import path
from .views import get_user_info
from .views import send_otp, verify_otp, create_user_after_payment

urlpatterns = [
    path('send-otp/', send_otp),
    path('verify-otp/', verify_otp),
     path('api/user-info/', get_user_info, name='user-info'),
    path('create-user/', create_user_after_payment),
]
