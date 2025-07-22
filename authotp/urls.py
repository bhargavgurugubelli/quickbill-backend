from django.urls import path
from .views import send_otp, verify_otp, create_user

urlpatterns = [
    path('send-otp/', send_otp, name='send_otp'),
    path('verify-otp/', verify_otp, name='verify_otp'),
    path('create-user/', create_user, name='create_user'),
]
