from django.db import models
from accounts.models import BaseOrder
from accounts.templatetags.custom_filters import romanize_division
import requests


class Overwatch2Rank(models.Model):
    rank_name = models.CharField(max_length=25)
    rank_image = models.ImageField(upload_to='overwatch2/images/', blank=True, null=True)

    def __str__(self):
        return self.rank_name
    
    def get_image_url(self):
        return f"/media/{self.rank_image}"

class Overwatch2Tier(models.Model):
    rank = models.OneToOneField(Overwatch2Rank, related_name='tier', on_delete=models.CASCADE)
    from_V_to_IV = models.FloatField(default=0)
    from_IV_to_III = models.FloatField(default=0)
    from_III_to_II = models.FloatField(default=0)
    from_II_to_I = models.FloatField(default=0)
    from_I_to_V_next = models.FloatField(default=0)

    def __str__(self):
        return f"Tiers for {self.rank.rank_name}"

class Overwatch2Mark(models.Model):
    rank = models.OneToOneField(Overwatch2Rank, related_name='mark', on_delete=models.CASCADE)
    mark_number = models.PositiveSmallIntegerField(default=5)
    mark_1 = models.FloatField(default=0)
    mark_2 = models.FloatField(default=0)
    mark_3 = models.FloatField(default=0)
    mark_4 = models.FloatField(default=0)
    mark_5 = models.FloatField(default=0)

    def __str__(self):
        return f"Mark for Rank: {self.rank.rank_name}"
    
class Overwatch2DivisionOrder(models.Model):
    DIVISION_CHOICES = [
        (1, 'V'),
        (2, 'IV'),
        (3, 'III'),
        (4, 'II'),
        (5, 'I'),
    ]
    MARKS_CHOISES = [
        (1 , '0-19 %'),
        (2 , '20-39 %'),
        (3 , '40-59 %'),
        (4 , '60-79 %'),
        (5 , '80-99 %'),
    ]
    ROLE_CHOISES = [
        (1 , 'DPS'),
        (2 , 'TANK'),
        (3 , 'SUPPORT'),
    ]
    order = models.OneToOneField(BaseOrder, on_delete=models.CASCADE, primary_key=True, default=None, related_name='overwatch2_order')
    current_rank = models.ForeignKey(Overwatch2Rank, on_delete=models.PROTECT, default=None, related_name='current_rank',blank=True, null=False)
    reached_rank = models.ForeignKey(Overwatch2Rank, on_delete=models.PROTECT, default=None, related_name='reached_rank',blank=True, null=True)
    desired_rank = models.ForeignKey(Overwatch2Rank, on_delete=models.PROTECT, default=None, related_name='desired_rank',blank=True, null=False)
    current_division = models.PositiveSmallIntegerField(choices=DIVISION_CHOICES,blank=True, null=False)
    reached_division = models.PositiveSmallIntegerField(choices=DIVISION_CHOICES,blank=True, null=True)
    desired_division = models.PositiveSmallIntegerField(choices=DIVISION_CHOICES,blank=True, null=False)
    current_marks = models.PositiveSmallIntegerField(choices=MARKS_CHOISES,blank=True, null=False)
    reached_marks = models.PositiveSmallIntegerField(choices=MARKS_CHOISES,blank=True, null=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOISES, null=False, blank=True, default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    # booster_champions = models.BooleanField(default=False, blank=True)


    def send_discord_notification(self):
        if self.order.status == 'Extend':
            return print('Extend Order')
        discord_webhook_url = 'https://discord.com/api/webhooks/1214543233200300083/R2-QI79E4K7UHxpOjbCGbGEytIl7PSmme9qY8flwBIvNraihcRLpTx3vB3qmCYVISLF4'
        current_time = self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        embed = {
            "title": "Overwatch 2",
            "description": (
                f"**Order ID:** {self.order.name}\n"
                f" From {str(self.current_rank).upper()} {romanize_division(self.current_division)} Marks {self.current_marks} "
                f" To {str(self.desired_rank).upper()} {romanize_division(self.desired_division)} server us" # change server next
            ),
            "color": 0xC0C0C0,  
            "footer": {"text": f"{current_time}"}, 
        }
        data = {
            "content": "New order has arrived \n",  
            "embeds": [embed],
        }
        headers = {
            "Content-Type": "application/json"
        }
        response = requests.post(discord_webhook_url, json=data, headers=headers)

        if response.status_code != 204:
            print(f"Failed to send Discord notification. Status code: {response.status_code}")

    def save_with_processing(self, *args, **kwargs):
        # self.order.game_id = 12
        # self.order.game_name = 'overwatch2'
        self.order.game_type = 'D'
        self.order.details = self.get_details()
        # 
        if not self.order.name:
            self.order.name = f'OVW2{self.order.id}'
        self.order.update_actual_price()
        self.order.save()
        super().save(*args, **kwargs)
        # self.send_discord_notification()
    
    def get_details(self):
        return f"From {str(self.current_rank).upper()} {romanize_division(self.current_division)} Marks {self.current_marks} To {str(self.desired_rank).upper()} {romanize_division(self.desired_division)}"

    def __str__(self):
        return self.get_details()
    
    
    def get_rank_value(self, *args, **kwargs):
        return f"{self.current_rank.id},{self.current_division},{self.current_marks},{self.desired_rank.id},{self.desired_division},{self.order.duo_boosting},{self.order.select_booster},{self.order.turbo_boost},{self.order.streaming}"


class Overwatch2Placement(models.Model):
  rank_name = models.CharField(max_length=25)
  rank_image = models.ImageField(upload_to='overwatch2/images/', blank=True, null=True)
  price = models.FloatField()

  def __str__(self):
    return self.rank_name
  
  def get_image_url(self):
    return f"/media/{self.rank_image}"

class Overwatch2PlacementOrder(models.Model):
  order = models.OneToOneField(BaseOrder, on_delete=models.CASCADE, primary_key=True, default=None, related_name='ovw2_placement_order')
  last_rank = models.ForeignKey(Overwatch2Placement, on_delete=models.CASCADE, default=None, related_name='ovw2_last_rank')
  number_of_match = models.IntegerField(default=5)

  choose_champions = models.BooleanField(default=False, blank=True, null=True)

  def send_discord_notification(self):
    if self.order.status == 'Extend':
        return print('Extend Order')
    discord_webhook_url ='https://discord.com/api/webhooks/1214543233200300083/R2-QI79E4K7UHxpOjbCGbGEytIl7PSmme9qY8flwBIvNraihcRLpTx3vB3qmCYVISLF4'
    current_time = self.created_at.strftime("%Y-%m-%d %H:%M:%S")
    embed = {
        "title": "OverWatch 2",
        "description": (
            f"**Order ID:** {self.order.name}\n"
            f"Placement {self.number_of_match} matchs with last rank {self.last_rank}"
        ),
        "color": 0xC0C0C0, 
        "footer": {"text": f"{current_time}"}, 
    }
    data = {
        "content": "New order has arrived \n",  
        "embeds": [embed],
    }


    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(discord_webhook_url, json=data, headers=headers)

    if response.status_code != 204:
        print(f"Failed to send Discord notification. Status code: {response.status_code}")


  def save_with_processing(self, *args, **kwargs):
    # self.order.game_id = 12
    # self.order.game_name = 'overwatch2'
    self.order.game_type = 'P'
    self.order.details = self.get_details()
    if not self.order.name:
      self.order.name = f'OVW2{self.order.id}'
    self.order.update_actual_price()
    self.order.save()
    super().save(*args, **kwargs)
    self.send_discord_notification()

  def get_details(self):
    return f"Boosting of {self.number_of_match} Placement Games With Last Rank {self.last_rank}"

  def __str__(self):
    return self.get_details() 