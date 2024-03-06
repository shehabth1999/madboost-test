from django.test import TestCase
from valorant.models import ValorantRank, ValorantTier, ValorantMark, ValorantPlacement

# Create your tests here.
class SetUp(TestCase):
  ranks = [
    ValorantRank(rank_name = 'iron', rank_image = 'valorant/images/iron.webp'),
    ValorantRank(rank_name = 'bronze', rank_image = 'valorant/images/bronze.webp'),
    ValorantRank(rank_name = 'silver', rank_image = 'valorant/images/silver.webp'),
    ValorantRank(rank_name = 'gold', rank_image = 'valorant/images/gold.webp'),
    ValorantRank(rank_name = 'platinum', rank_image = 'valorant/images/platinum.webp'),
    ValorantRank(rank_name = 'diamond', rank_image = 'valorant/images/diamond.webp'),
    ValorantRank(rank_name = 'ascendant', rank_image = 'valorant/images/ascendant.webp'),
    ValorantRank(rank_name = 'immortal', rank_image = 'valorant/images/immortal.webp'),
  ]

  tiers = [
    ValorantTier(rank_id = 1, from_I_to_II = 3, from_II_to_III = 3, from_III_to_I_next = 3),

    ValorantTier(rank_id = 2, from_I_to_II = 3.5, from_II_to_III = 3.5, from_III_to_I_next = 3.5),

    ValorantTier(rank_id = 3, from_I_to_II = 4, from_II_to_III = 4, from_III_to_I_next = 4),

    ValorantTier(rank_id = 4, from_I_to_II = 4.5, from_II_to_III = 4.5, from_III_to_I_next = 4.5),

    ValorantTier(rank_id = 5, from_I_to_II = 5, from_II_to_III = 5, from_III_to_I_next = 5),

    ValorantTier(rank_id = 6, from_I_to_II = 5.5, from_II_to_III = 5.5, from_III_to_I_next = 5.5),

    ValorantTier(rank_id = 7, from_I_to_II = 6, from_II_to_III = 6, from_III_to_I_next = 6),

    ValorantTier(rank_id = 8, from_I_to_II = 6.5, from_II_to_III = 6.5, from_III_to_I_next = 6.5),
  ]

  marks = [
    ValorantMark(rank_id = 1, marks_0_20 = 0.0, marks_21_40 = 0.2, marks_41_60 = 0.2, marks_61_80 = 0.2, marks_81_100 = 0.2),

    ValorantMark(rank_id = 2, marks_0_20 = 0.0, marks_21_40 = 0.3, marks_41_60 = 0.3, marks_61_80 = 0.3, marks_81_100 = 0.3),

    ValorantMark(rank_id = 3, marks_0_20 = 0.0, marks_21_40 = 0.4, marks_41_60 = 0.4, marks_61_80 = 0.4, marks_81_100 = 0.4),

    ValorantMark(rank_id = 4, marks_0_20 = 0.0, marks_21_40 = 0.5, marks_41_60 = 0.5, marks_61_80 = 0.5, marks_81_100 = 0.5),

    ValorantMark(rank_id = 5, marks_0_20 = 0.0, marks_21_40 = 0.6, marks_41_60 = 0.6, marks_61_80 = 0.6, marks_81_100 = 0.6),

    ValorantMark(rank_id = 6, marks_0_20 = 0.0, marks_21_40 = 0.7, marks_41_60 = 0.7, marks_61_80 = 0.7, marks_81_100 = 0.7),

    ValorantMark(rank_id = 7, marks_0_20 = 0.0, marks_21_40 = 0.8, marks_41_60 = 0.8, marks_61_80 = 0.8, marks_81_100 = 0.8),

    ValorantMark(rank_id = 8, marks_0_20 = 0.0, marks_21_40 = 0.9, marks_41_60 = 0.9, marks_61_80 = 0.9, marks_81_100 = 0.9),
  ]

  placements = [
    ValorantPlacement(rank_name = 'unrank', rank_image = 'valorant/images/unranked.webp', price = 4.31),
    ValorantPlacement(rank_name = 'iron', rank_image = 'valorant/images/iron.webp', price = 3.48),
    ValorantPlacement(rank_name = 'bronze', rank_image = 'valorant/images/bronze.webp', price = 3.48),
    ValorantPlacement(rank_name = 'silver', rank_image = 'valorant/images/silver.webp', price = 4.31),
    ValorantPlacement(rank_name = 'gold', rank_image = 'valorant/images/gold.webp', price = 5.17),
    ValorantPlacement(rank_name = 'platinum', rank_image = 'valorant/images/platinum.webp', price = 6.0),
    ValorantPlacement(rank_name = 'diamond', rank_image = 'valorant/images/diamond.webp', price =  7.74),
    ValorantPlacement(rank_name = 'ascendant', rank_image = 'valorant/images/ascendant.webp', price = 9.45),
    ValorantPlacement(rank_name = 'immortal', rank_image = 'valorant/images/immortal.webp', price = 11.17),
  ]

  ranks_queryset = ValorantRank.objects.bulk_create(ranks)
  tiers_queryset = ValorantTier.objects.bulk_create(tiers)
  marks_queryset = ValorantMark.objects.bulk_create(marks)
  placements_queryset = ValorantPlacement.objects.bulk_create(placements)