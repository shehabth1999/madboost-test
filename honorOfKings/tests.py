from django.test import TestCase
from honorOfKings.models import HonorOfKingsRank, HonorOfKingsTier, HonorOfKingsMark

# Create your tests here.
class SetUp(TestCase):
  ranks = [
    HonorOfKingsRank(rank_name = 'bronze', rank_image = 'hok/images/bronze.png'),
    HonorOfKingsRank(rank_name = 'silver', rank_image = 'hok/images/silver.png'),
    HonorOfKingsRank(rank_name = 'gold', rank_image = 'hok/images/gold.png'),
    HonorOfKingsRank(rank_name = 'platinum', rank_image = 'hok/images/platinum.png'),
    HonorOfKingsRank(rank_name = 'diamond', rank_image = 'hok/images/diamond.png'),
    HonorOfKingsRank(rank_name = 'king', rank_image = 'hok/images/king.png'),
  ]

  tiers = [
    HonorOfKingsTier(rank_id = 1, from_V_to_IV = 2.54,  from_IV_to_III = 2.54, from_III_to_II = 2.54, from_II_to_I = 2.54, from_I_to_IV_next = 2.54),

    HonorOfKingsTier(rank_id = 2, from_V_to_IV = 4.15, from_IV_to_III = 4.15, from_III_to_II = 4.15, from_II_to_I = 4.15, from_I_to_IV_next = 4.15),

    HonorOfKingsTier(rank_id = 3, from_V_to_IV = 5.8, from_IV_to_III = 5.8, from_III_to_II = 5.8, from_II_to_I = 5.8, from_I_to_IV_next = 9.06),

    HonorOfKingsTier(rank_id = 4, from_V_to_IV = 9.06, from_IV_to_III = 9.06, from_III_to_II = 9.06, from_II_to_I = 12.95, from_I_to_IV_next = 12.95),

    HonorOfKingsTier(rank_id = 5, from_V_to_IV = 12.95, from_IV_to_III = 12.95, from_III_to_II = 12.95, from_II_to_I = 12.95, from_I_to_IV_next = 19.42),

    HonorOfKingsTier(rank_id = 6, from_V_to_IV = 0, from_IV_to_III = 0, from_III_to_II = 27.78, from_II_to_I = 27.78, from_I_to_IV_next = 206.15),

  ]

  marks = [
    HonorOfKingsMark(rank_id = 1, star_1 = 0.2, star_2 = 0.2, star_3 = 0.2),

    HonorOfKingsMark(rank_id = 2, star_1 = 0.3, star_2 = 0.3, star_3 = 0.3),

    HonorOfKingsMark(rank_id = 3, star_1 = 0.4, star_2 = 0.4, star_3 = 0.4),

    HonorOfKingsMark(rank_id = 4, star_1 = 0.5, star_2 = 0.5, star_3 = 0.5),

    HonorOfKingsMark(rank_id = 5, star_1 = 0.6, star_2 = 0.6, star_3 = 0.6),

    HonorOfKingsMark(rank_id = 6, star_1 = 0.7, star_2 = 0.7, star_3 = 0.7),
  ]

  ranks_queryset = HonorOfKingsRank.objects.bulk_create(ranks)
  tiers_queryset = HonorOfKingsTier.objects.bulk_create(tiers)
  marks_queryset = HonorOfKingsMark.objects.bulk_create(marks)