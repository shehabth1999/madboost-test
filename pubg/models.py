from django.db import models
from accounts.models import BaseOrder
from accounts.templatetags.custom_filters import romanize_division, romanize_division_original
import requests

class PubgRank(models.Model):
  rank_name = models.CharField(max_length=25)
  rank_image = models.ImageField(upload_to='pubg/images/', blank=True, null=True)

  def __str__(self):
    return self.rank_name
    
  def get_image_url(self):
    return f"/media/{self.rank_image}"
  
class PubgTier(models.Model):
  rank = models.OneToOneField('PubgRank', related_name='tier', on_delete=models.CASCADE)
  from_V_to_VI = models.FloatField(default=0)
  from_VI_to_III = models.FloatField(default=0)
  from_III_to_II = models.FloatField(default=0)
  from_II_to_I = models.FloatField(default=0)

  def __str__(self):
    return f"Tiers for {self.rank.rank_name}"


class PubgMark(models.Model):
  rank = models.OneToOneField('PubgRank', related_name='mark', on_delete=models.CASCADE)
  marks_0_20 = models.FloatField(default=0)
  marks_21_40 = models.FloatField(default=0)
  marks_41_60 = models.FloatField(default=0)
  marks_61_80 = models.FloatField(default=0)
  marks_81_100 = models.FloatField(default=0)

  def __str__(self):
    return f"Marks for {self.rank}"
  
  
class PubgDivisionOrder(models.Model):
  DIVISION_CHOICES = [
    (1, 'I'),
    (2, 'II'),
    (3, 'III'),
    (4, 'IV'),
    (5, 'V'),
  ]
  MARKS_CHOISES = [
    (0, '0-20'),
    (1 , '21-40'),
    (2, '41-60'),
    (3, '61-80'),
    (4, '81-100')
  ]
  order = models.OneToOneField(BaseOrder, on_delete=models.CASCADE, primary_key=True, default=None, related_name='pubg_division_order')
  current_rank = models.ForeignKey(PubgRank, on_delete=models.CASCADE, default=None, related_name='current_rank',blank=True, null=True)
  reached_rank = models.ForeignKey(PubgRank, on_delete=models.CASCADE, default=None, related_name='reached_rank',blank=True, null=True)
  desired_rank = models.ForeignKey(PubgRank, on_delete=models.CASCADE, default=None, related_name='desired_rank',blank=True, null=True)
  current_division = models.PositiveSmallIntegerField(choices=DIVISION_CHOICES,blank=True, null=True)
  reached_division = models.PositiveSmallIntegerField(choices=DIVISION_CHOICES,blank=True, null=True)
  desired_division = models.PositiveSmallIntegerField(choices=DIVISION_CHOICES,blank=True, null=True)
  current_marks = models.PositiveSmallIntegerField(choices=MARKS_CHOISES,blank=True, null=True)
  reached_marks = models.PositiveSmallIntegerField(choices=MARKS_CHOISES,blank=True, null=True)
  created_at = models.DateTimeField(auto_now_add =True)

  select_champion = models.BooleanField(default=True, blank=True, null=True)

  def send_discord_notification(self):
    if self.order.status == 'Extend':
      return print('Extend Order')
    discord_webhook_url = 'https://discord.com/api/webhooks/1193142919620743258/fMYJS3jtU3Z2g8gON6UuHj9GKc1NEVRzor-8P9iWIMgNkiZTELCVfJysmXspeVHaSQxt'
    current_time = self.created_at.strftime("%Y-%m-%d %H:%M:%S")
    embed = {
      "title": "Pubg",
      "description": (
        f"**Order ID:** {self.order.name}\n"
        f" From {str(self.current_rank).upper()} {romanize_division(self.current_division)} Points"
        f" {str(self.current_rank).upper()} {romanize_division(self.current_division)} Points To {str(self.desired_rank).upper()} {romanize_division(self.desired_division)} server us" # change server next
      ),
      "color": 0x800080,  # Hex color code for a Discord color
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
    # self.order.game_id = 3
    # self.order.game_name = 'pubg'
    self.order.game_type = 'D'
    self.order.details = self.get_details()
    if not self.order.name:
      self.order.name = f'Pubg{self.order.id}'
    self.order.update_actual_price()
    self.order.save()
    super().save(*args, **kwargs)
    self.send_discord_notification()

  def get_details(self):
      return f"From {str(self.current_rank).upper()} {romanize_division_original(self.current_division)} Marks {self.current_marks} To {str(self.desired_rank).upper()} {romanize_division_original(self.desired_division)}"
  def __str__(self):
    return f"Boosting From {str(self.current_rank).upper()} {self.current_division} Marks {self.current_marks} To {str(self.desired_rank).upper()} {self.desired_division}"

  def get_rank_value(self, *args, **kwargs):
    return f"{self.current_rank.id},{self.current_division},{self.current_marks},{self.desired_rank.id},{self.desired_division},{self.order.duo_boosting},{self.order.select_booster},{self.order.turbo_boost},{self.order.streaming },{self.select_champion}"
