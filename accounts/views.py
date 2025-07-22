import random
from datetime import timedelta
from django.utils import timezone
from django.core.cache import cache
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

User = get_user_model()

@api_view(['POST'])
def send_otp(request):
    mobile = request.data.get('mobile')
    if not mobile:
        return Response({'error': 'Mobile number is required'}, status=400)

    otp = random.randint(100000, 999999)
    cache.set(f'otp_{mobile}', otp, timeout=300)  # 5 minutes

    print(f"OTP for {mobile} is: {otp}")  # Show OTP in console (dev mode)

    return Response({'message': 'OTP sent successfully'}, status=200)


@api_view(['POST'])
def verify_otp(request):
    mobile = request.data.get('mobile')
    entered_otp = request.data.get('otp')

    real_otp = cache.get(f'otp_{mobile}')

    if str(real_otp) != str(entered_otp):
        return Response({'error': 'Invalid OTP'}, status=400)

    try:
        user = User.objects.get(username=mobile)
        new_user = False
    except User.DoesNotExist:
        new_user = True  # Still needs payment

    return Response({'verified': True, 'new_user': new_user})


@api_view(['POST'])
def create_user_after_payment(request):
    mobile = request.data.get('mobile')

    if not mobile:
        return Response({'error': 'Mobile is required'}, status=400)

    # Check if user already exists
    if User.objects.filter(username=mobile).exists():
        return Response({'message': 'User already exists'}, status=200)

    # Create user (username = mobile, no password)
    user = User.objects.create_user(username=mobile, password=None)

    # ✅ Set 5-day free trial expiry
    user.free_trial_expiry = timezone.now() + timedelta(days=5)
    user.save()

    return Response({
        'message': 'User created successfully',
        'free_trial_expiry': user.free_trial_expiry
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_access(request):
    user = request.user
    now = timezone.now()

    # If user has free_trial_expiry and it's in the past
    if hasattr(user, 'free_trial_expiry') and user.free_trial_expiry < now:
        return Response({'access': False, 'message': 'Free trial expired'}, status=403)

    return Response({'access': True})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_info(request):
    user = request.user
    return Response({
        "mobile_number": user.mobile_number
    })