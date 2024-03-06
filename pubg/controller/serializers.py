from rest_framework import serializers

class DivisionSerializer(serializers.Serializer):
    current_rank = serializers.IntegerField(min_value=1, max_value=10)
    current_division = serializers.IntegerField(min_value=1, max_value=5)
    marks = serializers.IntegerField(min_value=0, max_value=4)
    desired_rank = serializers.IntegerField(min_value=1, max_value=10)
    desired_division = serializers.IntegerField(min_value=1, max_value=5)

    duo_boosting = serializers.BooleanField()
    select_booster = serializers.BooleanField()
    turbo_boost = serializers.BooleanField()
    streaming = serializers.BooleanField()
    select_champion = serializers.BooleanField()

    price = serializers.FloatField(min_value=10)

    choose_booster = serializers.IntegerField()

    extend_order = serializers.IntegerField()

    promo_code = serializers.CharField()
    server = serializers.CharField()