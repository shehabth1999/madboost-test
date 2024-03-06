from rest_framework import serializers
from accounts.models import PromoCode

class PromoCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromoCode
        fields = ['code', 'description', 'discount_amount', 'is_active']