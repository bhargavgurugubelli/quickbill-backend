from rest_framework import serializers

class SendOTPSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=15)
