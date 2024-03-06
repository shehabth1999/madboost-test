from django.test import TestCase
from pubg.models import PubgRank, PubgTier, PubgMark

# Create your tests here.
class SetUp(TestCase):
  ranks = [
    PubgRank(rank_name = 'bronze', rank_image = 'pubg/images/bronze.webp'),
    PubgRank(rank_name = 'silver', rank_image = 'pubg/images/silver.webp'),
    PubgRank(rank_name = 'gold', rank_image = 'pubg/images/gold.webp'),
    PubgRank(rank_name = 'platinum', rank_image = 'pubg/images/platinum.webp'),
    PubgRank(rank_name = 'diamond', rank_image = 'pubg/images/diamond.webp'),
    PubgRank(rank_name = 'master', rank_image = 'pubg/images/master.webp'),
  ]

  tiers = [
    PubgTier(rank_id = 1, from_V_to_VI = 5.0, from_VI_to_III = 5.0, from_III_to_II = 5.0, from_II_to_I = 5.0),

    PubgTier(rank_id = 2, from_V_to_VI = 5.33, from_VI_to_III = 6.33, from_III_to_II = 5.67, from_II_to_I = 5.0),

    PubgTier(rank_id = 3, from_V_to_VI = 6.67, from_VI_to_III = 6.67, from_III_to_II = 6.67, from_II_to_I = 6.67),

    PubgTier(rank_id = 4, from_V_to_VI = 10.0, from_VI_to_III = 10.0, from_III_to_II =10.0, from_II_to_I = 10.0),

    PubgTier(rank_id = 5, from_V_to_VI = 15.0, from_VI_to_III = 15.0, from_III_to_II = 15.0, from_II_to_I = 16.67),
  ]

  marks = [
    PubgMark(rank_id = 1, marks_0_20 = 0.0, marks_21_40 = 0.46, marks_41_60 = 0.47, marks_61_80 = 0.48, marks_81_100 = 0.49),

    PubgMark(rank_id = 2, marks_0_20 = 0.0, marks_21_40 = 0.51, marks_41_60 = 0.52, marks_61_80 = 0.53, marks_81_100 = 0.54),

    PubgMark(rank_id = 3, marks_0_20 = 0.0, marks_21_40 = 0.56, marks_41_60 = 0.57, marks_61_80 = 0.58, marks_81_100 = 0.59),

    PubgMark(rank_id = 4, marks_0_20 = 0.0, marks_21_40 = 0.61, marks_41_60 = 0.62, marks_61_80 = 0.63, marks_81_100 = 0.64),

    PubgMark(rank_id = 5, marks_0_20 = 0.0, marks_21_40 = 0.66, marks_41_60 = 0.67, marks_61_80 = 0.68, marks_81_100 = 0.69),
  ]

  ranks_queryset = PubgRank.objects.bulk_create(ranks)
  tiers_queryset = PubgTier.objects.bulk_create(tiers)
  marks_queryset = PubgMark.objects.bulk_create(marks)