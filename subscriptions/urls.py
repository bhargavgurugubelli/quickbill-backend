from django.urls import path
from .views import CreateSubscriberPaymentView

urlpatterns = [
    path('create-subscriber-payment/', CreateSubscriberPaymentView.as_view(), name='create-subscriber-payment'),
]
