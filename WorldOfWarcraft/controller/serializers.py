from rest_framework import serializers

class ArenaSerializer(serializers.Serializer):
    current_rank = serializers.IntegerField(min_value=1, max_value=4)
    current_RP = serializers.IntegerField(min_value=0, max_value=2500)
    desired_rank = serializers.IntegerField(min_value=1, max_value=4)
    desired_RP = serializers.IntegerField(min_value=1, max_value=2500)
    # is_Arena_2x2 = serializers.BooleanField()

    duo_boosting = serializers.BooleanField()
    select_booster = serializers.BooleanField()
    turbo_boost = serializers.BooleanField()
    streaming = serializers.BooleanField()
    choose_agents = serializers.BooleanField()

    price = serializers.FloatField(min_value=10)

    choose_booster = serializers.IntegerField()

    extend_order = serializers.IntegerField()