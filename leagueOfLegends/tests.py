from django.test import TestCase
from leagueOfLegends.models import LeagueOfLegendsRank, LeagueOfLegendsTier, LeagueOfLegendsMark, LeagueOfLegendsPlacement

# Create your tests here.
class SetUp(TestCase):
  ranks = [
    LeagueOfLegendsRank(rank_name = 'iron', rank_image = 'lol/images/iron.webp'),
    LeagueOfLegendsRank(rank_name = 'bronze', rank_image = 'lol/images/bronze.webp'),
    LeagueOfLegendsRank(rank_name = 'silver', rank_image = 'lol/images/silver.webp'),
    LeagueOfLegendsRank(rank_name = 'gold', rank_image = 'lol/images/gold.webp'),
    LeagueOfLegendsRank(rank_name = 'platinum', rank_image = 'lol/images/platinum.webp'),
    LeagueOfLegendsRank(rank_name = 'emerald', rank_image = 'lol/images/emerald.webp'),
    LeagueOfLegendsRank(rank_name = 'diamond', rank_image = 'lol/images/diamond.webp'),
    LeagueOfLegendsRank(rank_name = 'master', rank_image = 'lol/images/master.webp'),
  ]

  tiers = [
    LeagueOfLegendsTier(rank_id = 1, from_IV_to_III = 9.29, from_III_to_II = 9.29, from_II_to_I = 9.29, from_I_to_IV_next = 11.62),

    LeagueOfLegendsTier(rank_id = 2, from_IV_to_III = 13.69, from_III_to_II = 13.69, from_II_to_I = 13.69, from_I_to_IV_next = 72.77),

    LeagueOfLegendsTier(rank_id = 3, from_IV_to_III = 16.75, from_III_to_II = 16.75, from_II_to_I = 16.75, from_I_to_IV_next = 26.43),

    LeagueOfLegendsTier(rank_id = 4, from_IV_to_III = 29.57, from_III_to_II = 30.25, from_II_to_I = 36.42, from_I_to_IV_next = 36.42),

    LeagueOfLegendsTier(rank_id = 5, from_IV_to_III = 42.0, from_III_to_II = 45.26, from_II_to_I = 45.8, from_I_to_IV_next = 53.65),

    LeagueOfLegendsTier(rank_id = 6, from_IV_to_III = 54.62, from_III_to_II = 56.15, from_II_to_I = 56.15, from_I_to_IV_next = 64.62),

    LeagueOfLegendsTier(rank_id = 7, from_IV_to_III = 104.75, from_III_to_II = 142.46, from_II_to_I = 198.68, from_I_to_IV_next = 256.88),
  ]

  marks = [
    LeagueOfLegendsMark(rank_id = 1, marks_0_20 = 0.0, marks_21_40 = -0.11, marks_41_60 = 0.11, marks_61_80 = 0.11, marks_81_99 = 0.11, marks_series = 0.11),

    LeagueOfLegendsMark(rank_id = 2, marks_0_20 = 0.0, marks_21_40 = -0.11, marks_41_60 = 0.11, marks_61_80 = 0.11, marks_81_99 = 0.11, marks_series = 0.11),

    LeagueOfLegendsMark(rank_id = 3, marks_0_20 = 0.0, marks_21_40 = -0.11, marks_41_60 = 0.11, marks_61_80 = 0.11, marks_81_99 = 0.11, marks_series = 0.11),

    LeagueOfLegendsMark(rank_id = 4, marks_0_20 = 0.0, marks_21_40 = -0.11, marks_41_60 = 0.11, marks_61_80 = 0.11, marks_81_99 = 0.11, marks_series = 0.11),

    LeagueOfLegendsMark(rank_id = 5, marks_0_20 = 0.0, marks_21_40 = -0.11, marks_41_60 = 0.11, marks_61_80 = 0.11, marks_81_99 = 0.11, marks_series = 0.11),

    LeagueOfLegendsMark(rank_id = 6, marks_0_20 = 0.0, marks_21_40 = -0.11, marks_41_60 = 0.11, marks_61_80 = 0.11, marks_81_99 = 0.11, marks_series = 0.11),

    LeagueOfLegendsMark(rank_id = 7, marks_0_20 = 0.0, marks_21_40 = -0.11, marks_41_60 = 0.11, marks_61_80 = 0.11, marks_81_99 = 0.11, marks_series = 0.11),
  ]

  placements = [
    LeagueOfLegendsPlacement(rank_name = 'unrank', rank_image = '', price = 4.62),
    LeagueOfLegendsPlacement(rank_name = 'iron', rank_image = 'lol/images/iron.webp', price = 2.8),
    LeagueOfLegendsPlacement(rank_name = 'bronze', rank_image = 'lol/images/bronze.webp', price = 3.91),
    LeagueOfLegendsPlacement(rank_name = 'silver', rank_image = 'lol/images/silver.webp', price = 5.05),
    LeagueOfLegendsPlacement(rank_name = 'gold', rank_image = 'lol/images/gold.webp', price = 6.17),
    LeagueOfLegendsPlacement(rank_name = 'platinum', rank_image = 'lol/images/platinum.webp', price = 7.26),
    LeagueOfLegendsPlacement(rank_name = 'emerald', rank_image = 'lol/images/emerald.webp', price = 10.0),
    LeagueOfLegendsPlacement(rank_name = 'diamond', rank_image = 'lol/images/diamond.webp', price = 12.31),
    LeagueOfLegendsPlacement(rank_name = 'master', rank_image = 'lol/images/master.webp', price = 13.85),
  ]

  ranks_queryset = LeagueOfLegendsRank.objects.bulk_create(ranks)
  tiers_queryset = LeagueOfLegendsTier.objects.bulk_create(tiers)
  marks_queryset = LeagueOfLegendsMark.objects.bulk_create(marks)
  placements_queryset = LeagueOfLegendsPlacement.objects.bulk_create(placements)