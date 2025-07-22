from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_POST
from datetime import timedelta
import json
import random

from .models import OTPStorage  # ✅ Corrected model import
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

# Utility function to generate and send OTP
def send_otp_code(mobile):
    otp = str(random.randint(1000, 9999))
    OTPStorage.objects.create(mobile=mobile, otp=otp)
    print(f"Generated OTP for {mobile}: {otp}")  # ✅ For development only
    return otp

@csrf_exempt
@require_POST
def send_otp(request):
    data = json.loads(request.body)
    mobile = data.get('mobile')

    if not mobile:
        return JsonResponse({'error': 'Mobile number is required'}, status=400)

    send_otp_code(mobile)
    return JsonResponse({'message': 'OTP sent successfully'})

@csrf_exempt
@require_POST
def verify_otp(request):
    data = json.loads(request.body)
    mobile = data.get('mobile')
    otp = data.get('otp')

    if not mobile or not otp:
        return JsonResponse({'error': 'Mobile and OTP are required'}, status=400)

    try:
        record = OTPStorage.objects.filter(mobile=mobile).latest('created_at')
    except OTPStorage.DoesNotExist:
        return JsonResponse({'error': 'OTP not found for this number'}, status=404)

    if record.otp != otp:
        return JsonResponse({'error': 'Invalid OTP'}, status=400)

    if timezone.now() > record.created_at + timedelta(minutes=5):
        return JsonResponse({'error': 'OTP expired'}, status=400)

    try:
        user = User.objects.get(mobile=mobile)
        refresh = RefreshToken.for_user(user)
        return JsonResponse({
            'message': 'OTP verified. Existing user.',
            'token': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            },
            'user': {
                'id': user.id,
                'mobile': user.mobile
            },
            'existing_user': True
        })
    except User.DoesNotExist:
        return JsonResponse({
            'message': 'OTP verified. New user, proceed to payment.',
            'mobile': mobile,
            'existing_user': False
        })

@csrf_exempt
@require_POST
def create_user(request):
    data = json.loads(request.body)
    mobile = data.get('mobile')

    if not mobile:
        return JsonResponse({'error': 'Mobile number is required'}, status=400)

    if User.objects.filter(mobile=mobile).exists():
        return JsonResponse({'error': 'User already exists'}, status=400)

    user = User.objects.create_user(mobile=mobile)
    refresh = RefreshToken.for_user(user)

    return JsonResponse({
        'message': 'User created successfully',
        'token': {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        },
        'user': {
            'id': user.id,
            'mobile': user.mobile,
        }
    })
