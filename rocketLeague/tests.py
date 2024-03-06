from django.test import TestCase
from rocketLeague.models import RocketLeagueRank, RocketLeagueDivision, RocketLeaguePlacement, RocketLeagueSeasonal, RocketLeagueTournament

# Create your tests here.
class SetUp(TestCase):
  ranks = [
    RocketLeagueRank(rank_name = 'bronze', rank_image = 'rocketleague/images/bronze.webp'),
    RocketLeagueRank(rank_name = 'silver', rank_image = 'rocketleague/images/silver.webp'),
    RocketLeagueRank(rank_name = 'gold', rank_image = 'rocketleague/images/gold.webp'),
    RocketLeagueRank(rank_name = 'platinum', rank_image = 'rocketleague/images/platinum.webp'),
    RocketLeagueRank(rank_name = 'diamond', rank_image = 'rocketleague/images/diamond.webp'),
    RocketLeagueRank(rank_name = 'champion', rank_image = 'rocketleague/images/champion.webp'),
    RocketLeagueRank(rank_name = 'grand champion', rank_image = 'rocketleague/images/grand_champion.webp'),
    RocketLeagueRank(rank_name = 'supersonic legend', rank_image = 'rocketleague/images/supersonic_legend.webp'),
  ]

  divisions = [
    RocketLeagueDivision(rank_id = 1, from_I_to_II = 1.35, from_II_to_III = 1.35, from_III_to_I_next = 1.86),

    RocketLeagueDivision(rank_id = 2, from_I_to_II = 1.86, from_II_to_III = 3.41, from_III_to_I_next = 3.41),

    RocketLeagueDivision(rank_id = 3, from_I_to_II = 3.28, from_II_to_III = 3.28, from_III_to_I_next = 3.28),

    RocketLeagueDivision(rank_id = 4, from_I_to_II = 4.19, from_II_to_III = 4.07, from_III_to_I_next = 5.77),

    RocketLeagueDivision(rank_id = 5, from_I_to_II = 6.91, from_II_to_III = 10.88, from_III_to_I_next = 13.48),

    RocketLeagueDivision(rank_id = 6, from_I_to_II = 13.19, from_II_to_III = 13.62, from_III_to_I_next = 17.57),
    
    RocketLeagueDivision(rank_id = 7, from_I_to_II = 29.51, from_II_to_III = 40.82, from_III_to_I_next = 44.69),
  ]

  placements = [
    RocketLeaguePlacement(rank_name = 'bronze', rank_image = 'rocketleague/images/bronze.webp', price = 3.03),
    RocketLeaguePlacement(rank_name = 'silver', rank_image = 'rocketleague/images/silver.webp', price = 4.03),
    RocketLeaguePlacement(rank_name = 'gold', rank_image = 'rocketleague/images/gold.webp', price = 4.03),
    RocketLeaguePlacement(rank_name = 'platinum', rank_image = 'rocketleague/images/platinum.webp', price = 5.37),
    RocketLeaguePlacement(rank_name = 'diamond', rank_image = 'rocketleague/images/diamond.webp', price = 6.73),
    RocketLeaguePlacement(rank_name = 'champion', rank_image = 'rocketleague/images/champion.webp', price = 9.4),
    RocketLeaguePlacement(rank_name = 'grand champion', rank_image = 'rocketleague/images/grand_champion.webp', price = 16.11),
    RocketLeaguePlacement(rank_name = 'supersonic legend', rank_image = 'rocketleague/images/supersonic_legend.webp', price = 26.87),
  ]

  seasonals = [
    RocketLeagueSeasonal(rank_name = 'bronze', rank_image = 'rocketleague/images/bronze.webp', price = 2.03),
    RocketLeagueSeasonal(rank_name = 'silver', rank_image = 'rocketleague/images/silver.webp', price = 3.35),
    RocketLeagueSeasonal(rank_name = 'gold', rank_image = 'rocketleague/images/gold.webp', price = 3.35),
    RocketLeagueSeasonal(rank_name = 'platinum', rank_image = 'rocketleague/images/platinum.webp', price = 5.37),
    RocketLeagueSeasonal(rank_name = 'diamond', rank_image = 'rocketleague/images/diamond.webp', price = 6.73),
    RocketLeagueSeasonal(rank_name = 'champion', rank_image = 'rocketleague/images/champion.webp', price = 8.74),
    RocketLeagueSeasonal(rank_name = 'grand champion', rank_image = 'rocketleague/images/grand_champion.webp', price = 10.74),
    RocketLeagueSeasonal(rank_name = 'supersonic legend', rank_image = 'rocketleague/images/supersonic_legend.webp', price = 20.15),
  ]

  tournaments = [
    RocketLeagueTournament(rank_name = 'bronze', rank_image = 'rocketleague/images/bronze.webp', price = 20.15),
    RocketLeagueTournament(rank_name = 'silver', rank_image = 'rocketleague/images/silver.webp', price = 24.18),
    RocketLeagueTournament(rank_name = 'gold', rank_image = 'rocketleague/images/gold.webp', price = 33.58),
    RocketLeagueTournament(rank_name = 'platinum', rank_image = 'rocketleague/images/platinum.webp', price = 47.0),
    RocketLeagueTournament(rank_name = 'diamond', rank_image = 'rocketleague/images/diamond.webp', price = 53.73),
    RocketLeagueTournament(rank_name = 'champion', rank_image = 'rocketleague/images/champion.webp', price = 67.15),
    RocketLeagueTournament(rank_name = 'grand champion', rank_image = 'rocketleague/images/grand_champion.webp', price = 80.58),
    RocketLeagueTournament(rank_name = 'supersonic legend', rank_image = 'rocketleague/images/supersonic_legend.webp', price = 93.78),
  ]

  ranks_queryset = RocketLeagueRank.objects.bulk_create(ranks)
  divisions_queryset = RocketLeagueDivision.objects.bulk_create(divisions)
  placements_queryset = RocketLeaguePlacement.objects.bulk_create(placements)
  seasonals_queryset = RocketLeagueSeasonal.objects.bulk_create(seasonals)
  tournaments_queryset = RocketLeagueTournament.objects.bulk_create(tournaments)