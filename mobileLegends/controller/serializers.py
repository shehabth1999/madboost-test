from rest_framework import serializers

class DivisionSerializer(serializers.Serializer):
    current_rank = serializers.IntegerField(min_value=1, max_value=9)
    current_division = serializers.IntegerField(min_value=1, max_value=5)
    marks = serializers.IntegerField(min_value=0, max_value=5)
    desired_rank = serializers.IntegerField(min_value=1, max_value=10)
    desired_division = serializers.IntegerField(min_value=1, max_value=5)

    duo_boosting = serializers.BooleanField()
    select_booster = serializers.BooleanField()
    turbo_boost = serializers.BooleanField()
    streaming = serializers.BooleanField()

    price = serializers.FloatField(min_value=10)

    select_champion = serializers.BooleanField()

    extend_order = serializers.IntegerField()

    promo_code = serializers.CharField()
    server = serializers.CharField()

class PlacementSerializer(serializers.Serializer):
    last_rank = serializers.IntegerField(min_value=0, max_value=11)
    number_of_match = serializers.IntegerField(min_value=1, max_value=5)
    extend_order = serializers.IntegerField()
    promo_code = serializers.CharField()
    select_booster = serializers.BooleanField()
    server = serializers.CharField()
    select_champion = serializers.BooleanField()