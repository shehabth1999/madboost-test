from booster.models import Booster
from wildRift.models import WildRiftDivisionOrder
from valorant.models import ValorantDivisionOrder, ValorantPlacementOrder
from pubg.models import PubgDivisionOrder
from leagueOfLegends.models import LeagueOfLegendsDivisionOrder, LeagueOfLegendsPlacementOrder
from tft.models import TFTDivisionOrder, TFTPlacementOrder
from hearthstone.models import HearthstoneDivisionOrder
from rocketLeague.models import RocketLeagueDivisionOrder, RocketLeaguePlacementOrder, RocketLeagueSeasonalOrder, RocketLeagueTournamentOrder
from mobileLegends.models import MobileLegendsDivisionOrder, MobileLegendsPlacementOrder
from WorldOfWarcraft.models import WoWArenaBoostOrder
from overwatch2.models import Overwatch2DivisionOrder
from honorOfKings.models import HonorOfKingsDivisionOrder
from accounts.models import BaseOrder
from django.db.models import Model
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
channel_layer = get_channel_layer()


def check_rl_type(type) -> Model:
    ROCKET_LEAGUE_MODELS = {
    'D': RocketLeagueDivisionOrder,
    'P': RocketLeaguePlacementOrder,
    'S': RocketLeagueSeasonalOrder,
    'T': RocketLeagueTournamentOrder
        }
    Game = ROCKET_LEAGUE_MODELS.get(type, None)
    if not Game:
        raise ValueError(f"Invalid Rocket League game type: {type}")
    return Game

def check_valo_type(type) -> Model:
    VALORANT_MODELS = {
    'D': ValorantDivisionOrder,
    'P': ValorantPlacementOrder
        }
    Game = VALORANT_MODELS.get(type, None)
    if not Game:
        raise ValueError(f"Invalid Valorant game type: {type}")
    return Game

def check_lol_type(type) -> Model:
    LOL_MODELS = {
        'D': LeagueOfLegendsDivisionOrder,
        'P': LeagueOfLegendsPlacementOrder
    }
    Game = LOL_MODELS.get(type, None)
    if not Game:
        raise ValueError(f"Invalid League of Legends game type: {type}")
    return Game

def check_tft_type(type) -> Model:
    TFT_MODELS = {
        'D': TFTDivisionOrder,
        'P': TFTPlacementOrder
    }
    Game = TFT_MODELS.get(type, None)
    if not Game:
        raise ValueError(f"Invalid TFT game type: {type}")
    return Game

def check_mobleg_type(type) -> Model:
    MOBILE_LEGENDS_MODELS = {
        'D': MobileLegendsDivisionOrder,
        'P': MobileLegendsPlacementOrder
    }
    Game = MOBILE_LEGENDS_MODELS.get(type, None)
    if not Game:
        raise ValueError(f"Invalid Mobile Legends game type: {type}")
    return Game

def get_game(id, type) -> Model:
    GAME_MODELS = {
        1: WildRiftDivisionOrder,
        2: check_valo_type(type),
        3: PubgDivisionOrder,
        4: check_lol_type(type),
        5: check_tft_type(type),
        6: WoWArenaBoostOrder,
        7: HearthstoneDivisionOrder,
        8: check_mobleg_type(type),
        9: check_rl_type(type),
        10: 'dota2',
        11: HonorOfKingsDivisionOrder,
        12: Overwatch2DivisionOrder,
        13: 'csgo2',
    }
    Game = GAME_MODELS.get(id, None)
    if not Game:
        raise ValueError(f"Invalid game ID: {id}")
    return Game


def get_boosters(id):
    filter_conditions = {
    1: {'can_choose_me': True, 'is_wf_player': True},
    2: {'can_choose_me': True, 'is_valo_player': True},
    3: {'can_choose_me': True, 'is_pubg_player': True},
    4: {'can_choose_me': True, 'is_lol_player': True},
    5: {'can_choose_me': True, 'is_tft_player': True},
    6: {'can_choose_me': True, 'is_wow_player': True},
    7: {'can_choose_me': True, 'is_hearthstone_player': True},
    8: {'can_choose_me': True, 'is_mobleg_player': True},
    9: {'can_choose_me': True, 'is_rl_player': True},
    10: {'can_choose_me': True, 'is_dota2_player': True},
    11: {'can_choose_me': True, 'is_hok_player': True},
    12: {'can_choose_me': True, 'is_overwatch2_player': True},
    13: {'can_choose_me': True, 'is_csgo2_player': True},
    }
    filters = filter_conditions.get(id, {})
    boosters = Booster.objects.filter(**filters)
    return boosters


#--------------------------------------------------------------------------
def live_orders():
    orders = BaseOrder.objects.filter(booster=None).order_by('-created_at')
    all_orders_dict = []
    for order in orders:
        order_dict = {
            "id": order.pk,
            'name': order.game.name,
            'server': order.customer_server,
            'status': order.status,
            'price': order.price,
            'game_name':order.game.name,
            'details':order.details,
            'url':f'{order.game.link}/{order.pk}/',
        }
        all_orders_dict.append(order_dict)
    return all_orders_dict 

def refresh_order_page():
    all_orders_dict = live_orders()
    async_to_sync(channel_layer.group_send)(
        'orders',
        {
            'type': 'order_list',
            'order': all_orders_dict,
        }
    )
