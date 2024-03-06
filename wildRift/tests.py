from django.test import TestCase
from wildRift.models import WildRiftRank, WildRiftTier, WildRiftMark

# Create your tests here.
class SetUp(TestCase):
  ranks = [
    WildRiftRank(rank_name = 'iron', rank_image = 'wildrift/images/iron.webp'),
    WildRiftRank(rank_name = 'bronze', rank_image = 'wildrift/images/bronze.webp'),
    WildRiftRank(rank_name = 'silver', rank_image = 'wildrift/images/silver.webp'),
    WildRiftRank(rank_name = 'gold', rank_image = 'wildrift/images/gold.webp'),
    WildRiftRank(rank_name = 'platinum', rank_image = 'wildrift/images/platinum.webp'),
    WildRiftRank(rank_name = 'emerald', rank_image = 'wildrift/images/emerald.webp'),
    WildRiftRank(rank_name = 'diamond', rank_image = 'wildrift/images/diamond.webp'),
    WildRiftRank(rank_name = 'master', rank_image = 'wildrift/images/master.webp'),
  ]

  tiers = [
    WildRiftTier(rank_id = 1, from_IV_to_III = 2.54, from_III_to_II = 2.54, from_II_to_I = 2.54, from_I_to_IV_next = 2.54),

    WildRiftTier(rank_id = 2, from_IV_to_III = 4.15, from_III_to_II = 4.15, from_II_to_I = 4.15, from_I_to_IV_next = 4.15),

    WildRiftTier(rank_id = 3, from_IV_to_III = 5.8, from_III_to_II = 5.8, from_II_to_I = 5.8, from_I_to_IV_next = 9.06),

    WildRiftTier(rank_id = 4, from_IV_to_III = 9.06, from_III_to_II = 9.06, from_II_to_I = 12.95, from_I_to_IV_next = 12.95),

    WildRiftTier(rank_id = 5, from_IV_to_III = 12.95, from_III_to_II = 12.95, from_II_to_I = 12.95, from_I_to_IV_next = 19.42),

    WildRiftTier(rank_id = 6, from_IV_to_III = 27.78, from_III_to_II = 27.78, from_II_to_I = 27.78, from_I_to_IV_next = 206.15),

    WildRiftTier(rank_id = 7, from_IV_to_III = 48.12, from_III_to_II = 53.45, from_II_to_I = 76.8, from_I_to_IV_next = 85.32),

    WildRiftTier(rank_id = 8, from_IV_to_III =  85.32)

  ]

  marks = [
    WildRiftMark(rank_id = 1, tier_id = 1, mark_number = 2, mark_1 = 0.1, mark_2 = 0.11, mark_3 = 0.0, mark_4 = 0.0, mark_5 = 0.0, mark_6 = 0.0),

    WildRiftMark(rank_id = 2, tier_id = 2, mark_number = 3, mark_1 = 0.2, mark_2 = 0.21, mark_3 = 0.22, mark_4 = 0.0, mark_5 = 0.0, mark_6 = 0.0),

    WildRiftMark(rank_id = 3, tier_id = 3, mark_number = 3, mark_1 = 0.3, mark_2 = 0.31, mark_3 = 0.32, mark_4 = 0.0, mark_5 = 0.0, mark_6 = 0.0),

    WildRiftMark(rank_id = 4, tier_id = 4, mark_number = 4, mark_1 = 0.4, mark_2 = 0.41, mark_3 = 0.42, mark_4 = 0.43, mark_5 = 0.0, mark_6 = 0.0),

    WildRiftMark(rank_id = 5, tier_id = 5, mark_number = 4, mark_1 = 0.5, mark_2 = 0.51, mark_3 = 0.52, mark_4 = 0.53, mark_5 = 0.0, mark_6 = 0.0),

    WildRiftMark(rank_id = 6, tier_id = 6, mark_number = 5, mark_1 = 0.6, mark_2 = 0.61, mark_3 = 0.62, mark_4 = 0.63, mark_5 = 0.64, mark_6 = 0.0),

    WildRiftMark(rank_id = 7, tier_id = 7, mark_number = 6, mark_1 = 0.7, mark_2 = 0.71, mark_3 = 0.72, mark_4 = 0.73, mark_5 = 0.74, mark_6 = 0.75),
  ]

  ranks_queryset = WildRiftRank.objects.bulk_create(ranks)
  tiers_queryset = WildRiftTier.objects.bulk_create(tiers)
  marks_queryset = WildRiftMark.objects.bulk_create(marks)