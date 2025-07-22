from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Subscriber, Payment
from django.db import transaction

User = get_user_model()

class CreateSubscriberPaymentView(APIView):
    @transaction.atomic
    def post(self, request):
        data = request.data

        print("====== Incoming Payment Data ======")
        print(data)

        mobile = data.get('mobile')
        plan_id = data.get('plan_id')
        plan_name = data.get('plan_name')
        amount = data.get('amount')
        razorpay_payment_id = data.get('razorpay_payment_id')
        razorpay_order_id = data.get('razorpay_order_id')
        razorpay_signature = data.get('razorpay_signature')
        payment_status = data.get('payment_status')

        if not mobile:
            return Response({"error": "Mobile is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            subscriber, created = Subscriber.objects.get_or_create(mobile=mobile)
        except Exception as e:
            print("❌ Failed to get or create subscriber:", e)
            return Response({"error": "Failed to create subscriber"}, status=500)

        try:
            payment = Payment.objects.create(
                subscriber=subscriber,
                plan_id=plan_id,
                plan_name=plan_name,
                amount=amount,
                razorpay_payment_id=razorpay_payment_id,
                razorpay_order_id=razorpay_order_id,
                razorpay_signature=razorpay_signature,
                payment_status=payment_status,
            )
        except Exception as e:
            print("❌ Payment save failed:", e)
            return Response({"error": "Payment save failed"}, status=500)

        try:
            user, created = User.objects.get_or_create(mobile=mobile)
            if created:
                user.set_unusable_password()
                user.save()
        except Exception as e:
            print("❌ User creation failed:", e)
            return Response({"error": "User creation failed"}, status=500)

        try:
            if subscriber.user is None:
                subscriber.user = user
                subscriber.save()
        except Exception as e:
            print("❌ Linking subscriber to user failed:", e)
            return Response({"error": "Failed to link subscriber to user"}, status=500)

        try:
            refresh = RefreshToken.for_user(user)
            return Response({
                "token": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                "subscriber_id": subscriber.id,
                "payment_id": payment.id,
                "message": "Subscriber and payment created successfully"
            })
        except Exception as e:
            print("❌ Token generation failed:", e)
            return Response({"error": "Token generation failed"}, status=500)
