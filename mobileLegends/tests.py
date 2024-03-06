from django.test import TestCase
from mobileLegends.models import *

# Create your tests here.
class SetUp(TestCase):
  ranks = [
    MobileLegendsRank(rank_name = 'warrior', rank_image = 'lol/images/platinum.webp'),
    MobileLegendsRank(rank_name = 'elite', rank_image = 'lol/images/platinum.webp'),
    MobileLegendsRank(rank_name = 'master', rank_image = 'lol/images/platinum.webp'),
    MobileLegendsRank(rank_name = 'grandmaster', rank_image = 'lol/images/platinum.webp'),
    MobileLegendsRank(rank_name = 'epic', rank_image = 'lol/images/platinum.webp'),
    MobileLegendsRank(rank_name = 'legend', rank_image = 'lol/images/platinum.webp'),
    MobileLegendsRank(rank_name = 'mythic', rank_image = 'lol/images/platinum.webp'),
    MobileLegendsRank(rank_name = 'mythical honor', rank_image = 'lol/images/platinum.webp'),
    MobileLegendsRank(rank_name = 'mythical glory', rank_image = 'lol/images/platinum.webp'),
    MobileLegendsRank(rank_name = 'mythical immortal', rank_image = 'lol/images/platinum.webp'),
  ]


  ranks_queryset = MobileLegendsRank.objects.bulk_create(ranks)
#   tiers_queryset = LeagueOfLegendsTier.objects.bulk_create(tiers)
#   marks_queryset = LeagueOfLegendsMark.objects.bulk_create(marks)
#   placements_queryset = LeagueOfLegendsPlacement.objects.bulk_create(placements)