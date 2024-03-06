from django.test import TestCase
from tft.models import TFTRank, TFTTier, TFTMark, TFTPlacement

# Create your tests here.
class SetUp(TestCase):
  ranks = [
    TFTRank(rank_name = 'iron', rank_image = 'tft/images/iron.webp'),
    TFTRank(rank_name = 'bronze', rank_image = 'tft/images/bronze.webp'),
    TFTRank(rank_name = 'silver', rank_image = 'tft/images/silver.webp'),
    TFTRank(rank_name = 'gold', rank_image = 'tft/images/gold.webp'),
    TFTRank(rank_name = 'platinum', rank_image = 'tft/images/platinum.webp'),
    TFTRank(rank_name = 'emerald', rank_image = 'tft/images/emerald.webp'),
    TFTRank(rank_name = 'diamond', rank_image = 'tft/images/diamond.webp'),
    TFTRank(rank_name = 'master', rank_image = 'tft/images/master.webp'),
  ]

  tiers = [
    TFTTier(rank_id = 1, from_IV_to_III = 4.52, from_III_to_II = 4.52, from_II_to_I = 4.52, from_I_to_IV_next = 4.52),

    TFTTier(rank_id = 2, from_IV_to_III = 5.37, from_III_to_II = 5.37, from_II_to_I = 5.37, from_I_to_IV_next = 5.37),

    TFTTier(rank_id = 3, from_IV_to_III = 6.06, from_III_to_II = 6.06, from_II_to_I = 6.06, from_I_to_IV_next = 7.28),

    TFTTier(rank_id = 4, from_IV_to_III = 9.1, from_III_to_II = 10.0, from_II_to_I = 13.43, from_I_to_IV_next = 13.43),

    TFTTier(rank_id = 5, from_IV_to_III = 16.91, from_III_to_II = 18.22, from_II_to_I = 19.43, from_I_to_IV_next = 22.37),

    TFTTier(rank_id = 6, from_IV_to_III = 30.0, from_III_to_II = 31.67, from_II_to_I = 33.33, from_I_to_IV_next = 36.67),

    TFTTier(rank_id = 7, from_IV_to_III = 42.49, from_III_to_II = 51.43, from_II_to_I = 70.43, from_I_to_IV_next = 121.43),
  ]

  marks = [
    TFTMark(rank_id = 1, marks_0_20 = 0.0, marks_21_40 = 0.41, marks_41_60 = 0.42, marks_61_80 = 0.43, marks_81_100 = 0.44),

    TFTMark(rank_id = 2, marks_0_20 = 0.0, marks_21_40 = 0.46, marks_41_60 = 0.47, marks_61_80 = 0.48, marks_81_100 = 0.49),

    TFTMark(rank_id = 3, marks_0_20 = 0.0, marks_21_40 = 0.51, marks_41_60 = 0.52, marks_61_80 = 0.53, marks_81_100 = 0.54),

    TFTMark(rank_id = 4, marks_0_20 = 0.0, marks_21_40 = 0.56, marks_41_60 = 0.57, marks_61_80 = 0.58, marks_81_100 = 0.59),

    TFTMark(rank_id = 5, marks_0_20 = 0.0, marks_21_40 = 0.61, marks_41_60 = 0.62, marks_61_80 = 0.63, marks_81_100 = 0.64),

    TFTMark(rank_id = 6, marks_0_20 = 0.0, marks_21_40 = 0.66, marks_41_60 = 0.67, marks_61_80 = 0.68, marks_81_100 = 0.69),

    TFTMark(rank_id = 7, marks_0_20 = 0.0, marks_21_40 = 0.71, marks_41_60 = 0.72, marks_61_80 = 0.73, marks_81_100 = 0.74),

  ]

  placements = [
    TFTPlacement(rank_name = 'unrank', rank_image = 'tft/images/unranked.webp', price = 5.17),
    TFTPlacement(rank_name = 'iron', rank_image = 'tft/images/iron.webp', price = 5.17),
    TFTPlacement(rank_name = 'bronze', rank_image = 'tft/images/bronze.webp', price = 5.17),
    TFTPlacement(rank_name = 'silver', rank_image = 'tft/images/silver.webp', price = 5.17),
    TFTPlacement(rank_name = 'gold', rank_image = 'tft/images/gold.webp', price = 5.17),
    TFTPlacement(rank_name = 'platinum', rank_image = 'tft/images/platinum.webp', price = 5.83),
    TFTPlacement(rank_name = 'emerald', rank_image = 'tft/images/emerald.webp', price = 10.0),
    TFTPlacement(rank_name = 'diamond', rank_image = 'tft/images/diamond.webp', price =  6.27),
    TFTPlacement(rank_name = 'master', rank_image = 'tft/images/master.webp', price = 8.33),
  ]

  ranks_queryset = TFTRank.objects.bulk_create(ranks)
  tiers_queryset = TFTTier.objects.bulk_create(tiers)
  marks_queryset = TFTMark.objects.bulk_create(marks)
  placements_queryset = TFTPlacement.objects.bulk_create(placements)