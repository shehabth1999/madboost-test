from rest_framework import serializers

class RankBoostSerializer(serializers.Serializer):

    # rank
    # current_rank = serializers.IntegerField(min_value=1, max_value=4)
    # desired_rank = serializers.IntegerField(min_value=1, max_value=4)
    
    # no need to get rank we know rank from divisions

    # division
    current_division = serializers.IntegerField(min_value=0, max_value=2500)
    desired_division = serializers.IntegerField(min_value=1, max_value=2500)

    # exra filds about order
    duo_boosting = serializers.BooleanField()
    select_booster = serializers.BooleanField()
    turbo_boost = serializers.BooleanField()
    streaming = serializers.BooleanField()
    choose_booster = serializers.IntegerField()
    extend_order = serializers.IntegerField()

    server = serializers.CharField()
    promo_code = serializers.CharField()



    # fild not fo all games
    select_champion = serializers.BooleanField()
    role = serializers.IntegerField(min_value=1, max_value=2)