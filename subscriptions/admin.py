from django.contrib import admin
from .models import Subscriber, Payment

@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('mobile', 'get_user_mobile')
    search_fields = ('mobile', 'user__mobile')
    list_filter = ('user',)

    def get_user_mobile(self, obj):
        return obj.user.mobile if obj.user else 'Not Linked'
    get_user_mobile.short_description = 'Linked User Mobile'


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('subscriber', 'plan_name', 'amount', 'payment_status', 'created_at', 'get_user_mobile')
    list_filter = ('payment_status', 'created_at')
    search_fields = ('subscriber__mobile', 'plan_name', 'razorpay_payment_id', 'razorpay_order_id')

    def get_user_mobile(self, obj):
        return obj.subscriber.user.mobile if obj.subscriber.user else 'Not Linked'
    get_user_mobile.short_description = 'User Mobile'
