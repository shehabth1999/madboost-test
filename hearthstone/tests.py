from django.test import TestCase
from hearthstone.models import HearthstoneRank, HearthstoneTier, HearthstoneMark

class SetUp(TestCase):
  ranks = [
    HearthstoneRank(rank_name = 'bronze', rank_image = 'hearthstone/images/bronze.webp'),
    HearthstoneRank(rank_name = 'silver', rank_image = 'hearthstone/images/silver.webp'),
    HearthstoneRank(rank_name = 'gold', rank_image = 'hearthstone/images/gold.webp'),
    HearthstoneRank(rank_name = 'platinum', rank_image = 'hearthstone/images/platinum.webp'),
    HearthstoneRank(rank_name = 'diamond', rank_image = 'hearthstone/images/diamond.webp'),
    HearthstoneRank(rank_name = 'legend', rank_image = 'hearthstone/images/legend.webp'),
  ]
  
  tiers = [
    HearthstoneTier(rank_id = 1, from_X_to_IX = 1.43, from_IX_to_VIII = 1.43, from_VIII_to_VII = 1.43, from_VII_to_VI = 1.43, from_VI_to_V = 1.43, from_V_to_IV = 1.43, from_IV_to_III = 1.43, from_III_to_II = 1.43, from_II_to_I = 1.43, from_I_to_IV_next = 1.43),

    HearthstoneTier(rank_id = 2, from_X_to_IX = 1.43, from_IX_to_VIII = 1.43, from_VIII_to_VII = 1.43, from_VII_to_VI = 1.43, from_VI_to_V = 1.43, from_V_to_IV = 1.43, from_IV_to_III = 1.43, from_III_to_II = 1.43, from_II_to_I = 1.43, from_I_to_IV_next = 1.43),

    HearthstoneTier(rank_id = 3, from_X_to_IX = 1.43, from_IX_to_VIII = 1.43, from_VIII_to_VII = 1.43, from_VII_to_VI = 1.43, from_VI_to_V = 1.43, from_V_to_IV = 1.43, from_IV_to_III = 1.43, from_III_to_II = 1.43, from_II_to_I = 2.15, from_I_to_IV_next = 2.15),

    HearthstoneTier(rank_id = 4, from_X_to_IX = 2.87, from_IX_to_VIII = 2.87, from_VIII_to_VII = 2.87, from_VII_to_VI = 2.87, from_VI_to_V = 2.87, from_V_to_IV = 2.87, from_IV_to_III = 2.873, from_III_to_II = 2.87, from_II_to_I = 2.87, from_I_to_IV_next = 2.87),

    HearthstoneTier(rank_id = 5, from_X_to_IX = 3.56, from_IX_to_VIII = 3.56, from_VIII_to_VII = 3.56, from_VII_to_VI = 3.56, from_VI_to_V = 3.56, from_V_to_IV = 3.56, from_IV_to_III = 4.28, from_III_to_II = 4.28, from_II_to_I = 4.28, from_I_to_IV_next = 4.28),
  ]

  marks = [
    HearthstoneMark(rank_id = 1, marks_3 = 0, marks_2 = 0.5, marks_1 = 0.52),
    HearthstoneMark(rank_id = 2, marks_3 = 0, marks_2 = 0.53, marks_1 = 0.54),
    HearthstoneMark(rank_id = 3, marks_3 = 0, marks_2 = 0.55, marks_1 = 0.56),
    HearthstoneMark(rank_id = 4, marks_3 = 0, marks_2 = 0.57, marks_1 = 0.58),
    HearthstoneMark(rank_id = 5, marks_3 = 0, marks_2 = 0.59, marks_1 = 0.6),
  ]

  ranks_queryset = HearthstoneRank.objects.bulk_create(ranks)
  tiers_queryset = HearthstoneTier.objects.bulk_create(tiers)
  marks_queryset = HearthstoneMark.objects.bulk_create(marks)