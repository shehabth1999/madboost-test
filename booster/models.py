from django.db import models
from accounts.models import BaseUser, BaseOrder
from wildRift.models import WildRiftRank
from valorant.models import ValorantRank
from pubg.models import PubgRank
from leagueOfLegends.models import LeagueOfLegendsRank
from tft.models import TFTRank
from hearthstone.models import HearthstoneRank
from rocketLeague.models import RocketLeagueRank
from mobileLegends.models import MobileLegendsRank
from WorldOfWarcraft.models import WoWRank
from overwatch2.models import Overwatch2Rank

class OrderRating(models.Model):
    customer = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name='ratings_given')
    booster = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name='ratings_received', limit_choices_to={'is_booster': True})
    rate = models.IntegerField(default=0)
    text = models.TextField(null=True, max_length=500)
    game = models.IntegerField(default=1)
    anonymous = models.BooleanField(default=False)
    order = models.OneToOneField(BaseOrder, on_delete=models.CASCADE, related_name='order_rated')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Set customer and booster based on the associated order
        self.customer = self.order.customer
        self.booster = self.order.booster

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.customer.username} rated {self.booster.username} with {self.rate}'
    

class Booster(models.Model):
    booster = models.OneToOneField(BaseUser, on_delete=models.CASCADE, related_name='booster', null=True,  limit_choices_to={'is_booster': True})
    image = models.ImageField(null=True,upload_to='media/booster/', blank= True)
    about_you = models.TextField(max_length=1000,null=True, blank=True)
    can_choose_me = models.BooleanField(default=True ,blank=True)
    email_verified_at = models.DateTimeField(null=True,blank=True)
    is_wf_player = models.BooleanField(default=False)
    is_valo_player = models.BooleanField(default=False)
    is_pubg_player = models.BooleanField(default=False)
    is_lol_player = models.BooleanField(default=False)
    is_tft_player = models.BooleanField(default=False)
    is_hearthstone_player = models.BooleanField(default=False)
    is_rl_player = models.BooleanField(default=False)
    is_mobleg_player = models.BooleanField(default=False)
    is_wow_player = models.BooleanField(default=False)
    is_overwatch2_player = models.BooleanField(default=False)
    is_dota2_player = models.BooleanField(default=False)
    is_hok_player = models.BooleanField(default=False)
    is_csgo2_player = models.BooleanField(default=False)
    achived_rank_wr = models.ForeignKey(WildRiftRank, on_delete=models.SET_NULL, null=True, blank=True, related_name='wr_rank')
    achived_rank_valo = models.ForeignKey(ValorantRank, on_delete=models.SET_NULL, null=True, blank=True, related_name='valo_rank')
    achived_rank_pubg = models.ForeignKey(PubgRank, on_delete=models.SET_NULL, null=True, blank=True, related_name='pubg_rank')
    achived_rank_lol = models.ForeignKey(LeagueOfLegendsRank, on_delete=models.SET_NULL, null=True, blank=True, related_name='lol_rank')
    achived_rank_tft = models.ForeignKey(TFTRank, on_delete=models.SET_NULL, null=True, blank=True, related_name='tft_rank')
    achived_rank_hearthstone = models.ForeignKey(HearthstoneRank, on_delete=models.SET_NULL, null=True, blank=True, related_name='hearthstone_rank')
    achived_rank_rl= models.ForeignKey(RocketLeagueRank, on_delete=models.SET_NULL, null=True, blank=True, related_name='rl_rank')
    achived_rank_modleg = models.ForeignKey(MobileLegendsRank, on_delete = models.SET_NULL, null=True, blank=True, related_name='mobleg_rank')
    achived_rank_wow = models.ForeignKey(WoWRank, on_delete = models.SET_NULL, null=True, blank=True, related_name='wow_rank')
    achived_rank_overwatch2 = models.ForeignKey(Overwatch2Rank, on_delete = models.SET_NULL, null=True, blank=True, related_name='overwatch2_rank')
    
    
    # achived_rank_dota2= models.ForeignKey(, on_delete = models.SET_NULL, null=True, blank=True, related_name='dota2_rank')
    # achived_rank_hok = models.ForeignKey(, on_delete = models.SET_NULL, null=True, blank=True, related_name='hok_rank')
    # achived_rank_csgo2 = models.ForeignKey(, on_delete = models.SET_NULL, null=True, blank=True, related_name='csgo2_rank')
    
    def __str__(self):
        return f'{self.booster.username}'
    
    def save(self, *args, **kwargs):
        # When saving a Booster instance, set is_booster to True for the associated BaseUser
        self.booster.is_booster = True
        self.booster.save()
        super().save(*args, **kwargs)
