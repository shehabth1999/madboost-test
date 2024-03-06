# serializers.py
from rest_framework import serializers
from booster.models import OrderRating
from accounts.models import BaseUser

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderRating
        fields = ['rate', 'text', 'anonymous']

class CanChooseMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseUser
        fields = ['can_choose_me']