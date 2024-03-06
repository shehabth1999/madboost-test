from rest_framework import serializers

class RankSerializer(serializers.Serializer):
    current_rank = serializers.IntegerField(min_value=1, max_value=7)
    current_division = serializers.IntegerField(min_value=1, max_value=4)

    marks = serializers.IntegerField(min_value=0, max_value=5)
    
    desired_rank = serializers.IntegerField(min_value=1, max_value=8)
    desired_division = serializers.IntegerField(min_value=1, max_value=4)

    server = serializers.CharField(max_length=300)

    duo_boosting = serializers.BooleanField()
    select_booster = serializers.BooleanField()
    turbo_boost = serializers.BooleanField()
    streaming = serializers.BooleanField()
    booster_champions = serializers.BooleanField()

    price = serializers.FloatField(min_value=10)

    choose_booster = serializers.IntegerField()

    extend_order = serializers.IntegerField()

    promo_code = serializers.CharField()


class PlacementSerializer(serializers.Serializer):
    Previous_Season_Rank = serializers.IntegerField()
    games_count = serializers.IntegerField()
    promo_code = serializers.CharField()
    