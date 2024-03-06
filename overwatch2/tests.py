from django.test import TestCase
from overwatch2.models import Overwatch2Rank, Overwatch2Tier, Overwatch2Mark, Overwatch2Placement
# Create your tests here.
class SetUp(TestCase):
  ranks = [
    Overwatch2Rank(rank_name = 'bronze', rank_image = 'overwatch2/images/bronze.png'),
    Overwatch2Rank(rank_name = 'silver', rank_image = 'overwatch2/images/silver.png'),
    Overwatch2Rank(rank_name = 'gold', rank_image = 'overwatch2/images/gold.png'),
    Overwatch2Rank(rank_name = 'platinum', rank_image = 'overwatch2/images/paltinum.png'),
    Overwatch2Rank(rank_name = 'diamond', rank_image = 'overwatch2/images/diamond.png'),
    Overwatch2Rank(rank_name = 'master', rank_image = 'overwatch2/images/master.png'),
    Overwatch2Rank(rank_name = 'grand master', rank_image = 'overwatch2/images/grandmaster.png'),
    Overwatch2Rank(rank_name = 'champion', rank_image = 'overwatch2/images/unranked.webp'),
  ]

  tiers = [
    Overwatch2Tier(rank_id = 1, from_V_to_IV = 13.69, from_IV_to_III = 9.29, from_III_to_II = 9.29, from_II_to_I = 9.29, from_I_to_V_next = 11.62),

    Overwatch2Tier(rank_id = 2, from_V_to_IV = 13.69, from_IV_to_III = 13.69, from_III_to_II = 13.69, from_II_to_I = 13.69, from_I_to_V_next = 72.77),

    Overwatch2Tier(rank_id = 3, from_V_to_IV = 16.75, from_IV_to_III = 16.75, from_III_to_II = 16.75, from_II_to_I = 16.75, from_I_to_V_next = 26.43),

    Overwatch2Tier(rank_id = 4, from_V_to_IV = 29.57, from_IV_to_III = 29.57, from_III_to_II = 30.25, from_II_to_I = 36.42, from_I_to_V_next = 36.42),

    Overwatch2Tier(rank_id = 5, from_V_to_IV = 42.0, from_IV_to_III = 42.0, from_III_to_II = 45.26, from_II_to_I = 45.8, from_I_to_V_next = 53.65),

    Overwatch2Tier(rank_id = 6, from_V_to_IV = 54.62, from_IV_to_III = 54.62, from_III_to_II = 56.15, from_II_to_I = 56.15, from_I_to_V_next = 64.62),

    Overwatch2Tier(rank_id = 7, from_V_to_IV = 60.0, from_IV_to_III = 104.75, from_III_to_II = 142.46, from_II_to_I = 198.68, from_I_to_V_next = 256.88),

    Overwatch2Tier(rank_id = 8, from_V_to_IV = 70.0, from_IV_to_III = 130.75, from_III_to_II = 142.46, from_II_to_I = 198.68, from_I_to_V_next = 256.88),
  ]

  marks = [
    Overwatch2Mark(rank_id = 1, mark_1 = 1, mark_2 = 2, mark_3 = 3, mark_4 = 4, mark_5 = 5),
    
    Overwatch2Mark(rank_id = 2, mark_1 = 2, mark_2 = 4, mark_3 = 6, mark_4 = 8, mark_5 = 10),

    Overwatch2Mark(rank_id = 3, mark_1 = 3, mark_2 = 6, mark_3 = 9, mark_4 = 15, mark_5 = 18),

    Overwatch2Mark(rank_id = 4, mark_1 = 4, mark_2 = 8, mark_3 = 12, mark_4 = 16, mark_5 = 18),

    Overwatch2Mark(rank_id = 5, mark_1 = 10, mark_2 = 13, mark_3 = 17, mark_4 = 19, mark_5 = 20),

  ]

  placements = [
    Overwatch2Placement(rank_name = 'unrank', rank_image = 'overwatch2/images/unranked.webp', price = 4.62),
    Overwatch2Placement(rank_name = 'bronze', rank_image = 'overwatch2/images/bronze.png', price = 3.91),
    Overwatch2Placement(rank_name = 'silver', rank_image = 'overwatch2/images/silver.png', price = 5.05),
    Overwatch2Placement(rank_name = 'gold', rank_image = 'overwatch2/images/gold.png', price = 6.17),
    Overwatch2Placement(rank_name = 'platinum', rank_image = 'overwatch2/images/paltinum.png', price = 7.26),
    Overwatch2Placement(rank_name = 'diamond', rank_image = 'overwatch2/images/diamond.png', price = 12.31),
    Overwatch2Placement(rank_name = 'master', rank_image = 'overwatch2/images/master.png', price = 13.85),
    Overwatch2Placement(rank_name = 'grand master', rank_image = 'overwatch2/images/grandmaster.png', price = 20.85),
    Overwatch2Placement(rank_name = 'champion', rank_image = 'overwatch2/images/unranked.webp', price = 30),
  ]

  ranks_queryset = Overwatch2Rank.objects.bulk_create(ranks)
  tiers_queryset = Overwatch2Tier.objects.bulk_create(tiers)
  marks_queryset = Overwatch2Mark.objects.bulk_create(marks)
  placements_queryset = Overwatch2Placement.objects.bulk_create(placements)