from django.test import TestCase
from games.models import Game

# Create your tests here.
class SetUp(TestCase):
  games = [
    Game(name='Lol: Wild Rift', link='wildRift', logo_image='games/logos/WildRift.png', banner_image='games/banners/WildRift.png', name_image='games/names/WildRift.png'),

    Game(name='VALORANT', link='valorant', logo_image='games/logos/Valorant.png', banner_image='games/banners/Valorant.png', name_image='games/names/Valorant.png'),

    Game(name='Pubg Mobile', link='pubg', logo_image='games/logos/Pubg.png', banner_image='games/banners/Pubg.png', name_image='games/names/Pubg.png'),

    Game(name='League of Legends', link='lol', logo_image='games/logos/LOL.png', banner_image='games/banners/LOL.png', name_image='games/names/LOL.png'),

    Game(name='Team Fight Tactics', link='tft', logo_image='games/logos/TFT.png', banner_image='games/banners/TFT.png', name_image='games/names/TFT.png'),

    Game(name='World of Warcraft', link='wow', logo_image='games/logos/WOW.png', banner_image='games/banners/WOW.png', name_image='games/names/WOW.png'),

    Game(name='Hearthstone', link='hearthstone', logo_image='games/logos/Hearthstone.png', banner_image='games/banners/Hearthstone.png', name_image='games/names/Hearthstone.png'),

    Game(name='Mobile Legends', link='mobileLegends', logo_image='games/logos/MobileLegends.png', banner_image='games/banners/MobileLegends.png', name_image='games/names/MobileLegends.png'),

    Game(name='Rocket League', link='rocketLeague', logo_image='games/logos/RocketLeague.png', banner_image='games/banners/RocketLeague.png', name_image='games/names/RocketLeague.png'),

    Game(name='Dota 2', link='dota2', logo_image='games/logos/Dota2.png', banner_image='games/banners/Dota2.png', name_image='games/names/Dota2.png'),

    Game(name='Honer Of King', link='hok', logo_image='games/logos/HonorOfKings.png', banner_image='games/banners/HonorOfKings.png', name_image='games/names/HonorOfKings.png'),

    Game(name='Overwatch 2', link='overwatch2', logo_image='games/logos/Overwatch2.png', banner_image='games/banners/Overwatch2.png', name_image='games/names/Overwatch2.png'),

    Game(name='CS GO 2', link='csgo2', logo_image='games/logos/CS2.png', banner_image='games/banners/CS2.png', name_image='games/names/CS2.png'),
  ]

  games_queryset = Game.objects.bulk_create(games)