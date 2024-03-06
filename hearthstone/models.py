from django.db import models
from accounts.models import BaseOrder, Wallet
from accounts.templatetags.custom_filters import ten_romanize_division,romanize_division
import requests


# Create your models here.
class HearthstoneRank(models.Model):
  rank_name = models.CharField(max_length=25)
  rank_image = models.ImageField(upload_to='hearthstone/images/', blank=True, null=True)

  def __str__(self):
    return self.rank_name
    
  def get_image_url(self):
    return f"/media/{self.rank_image}"
  
class HearthstoneTier(models.Model):
  rank = models.OneToOneField('HearthstoneRank', related_name='tier', on_delete=models.CASCADE)
  from_X_to_IX = models.FloatField(default=0)
  from_IX_to_VIII = models.FloatField(default=0)
  from_VIII_to_VII = models.FloatField(default=0)
  from_VII_to_VI = models.FloatField(default=0)
  from_VI_to_V = models.FloatField(default=0)
  from_V_to_IV = models.FloatField(default=0)
  from_IV_to_III = models.FloatField(default=0)
  from_III_to_II = models.FloatField(default=0)
  from_II_to_I = models.FloatField(default=0)
  from_I_to_IV_next = models.FloatField(default=0)

  def __str__(self):
    return f"Tiers for {self.rank.rank_name}"

class HearthstoneMark(models.Model):
  rank = models.OneToOneField('HearthstoneRank', related_name='mark', on_delete=models.CASCADE)
  marks_3 = models.FloatField(default=0)
  marks_2 = models.FloatField(default=0)
  marks_1 = models.FloatField(default=0)

  def __str__(self):
    return f"{self.rank} -> Marks 3: {self.marks_3}, Marks 2 : {self.marks_2}, Marks 1 : {self.marks_1}"
  
class HearthstoneDivisionOrder(models.Model):
  DIVISION_CHOICES = [
    (1, 'X'),
    (2, 'IX'),
    (3, 'VIII'),
    (4, 'VII'),
    (5, 'VI'),
    (6, 'V'),
    (7, 'IV'),
    (8, 'III'),
    (9, 'II'),
    (10, 'I'),
  ]
  MARKS_CHOISES = [
    (0, '3'),
    (1 , '2'),
    (2, '1'),
  ]
  order = models.OneToOneField(BaseOrder, on_delete=models.CASCADE, primary_key=True, default=None, related_name='hearthstone_division_order')
  current_rank = models.ForeignKey(HearthstoneRank, on_delete=models.CASCADE, default=None, related_name='current_rank',blank=True, null=True)
  reached_rank = models.ForeignKey(HearthstoneRank, on_delete=models.CASCADE, default=None, related_name='reached_rank',blank=True, null=True)
  desired_rank = models.ForeignKey(HearthstoneRank, on_delete=models.CASCADE, default=None, related_name='desired_rank',blank=True, null=True)
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
    discord_webhook_url = 'https://discordapp.com/api/webhooks/1209758608599031858/PtdjMTcZq9dR5lo9uTVX-cJPSPEduMXcUjoiQrMchDHvyHv0oTuZnCIVIcsX6dwqGCy3'
    current_time = self.created_at.strftime("%Y-%m-%d %H:%M:%S")
    embed = {
        "title": "Rift",
        "description": (
            f"**Order ID:** {self.order.name}\n"
            f" From {str(self.current_rank).upper()} {romanize_division(self.current_division)} Marks {self.current_marks} "
            f" To {str(self.desired_rank).upper()} {romanize_division(self.desired_division)}\n server us" # change server next
        ),
        "color": 0x3498db,  # Hex color code for a Discord blue color
        "footer": {"text": f"{current_time}"}, 
    }
    data = {
        "content": "New order has arrived \n",  # Set content to a space if you only want to send an embed
        "embeds": [embed],
    }


    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(discord_webhook_url, json=data, headers=headers)

    if response.status_code != 204:
        print(f"Failed to send Discord notification. Status code: {response.status_code}")


  def save_with_processing(self, *args, **kwargs):
    # self.order.game_id = 7
    # self.order.game_name = 'hearthstone'
    self.order.game_type = 'D'
    self.order.details = self.get_details()
    if not self.order.name:
      self.order.name = f'HEARTHSTONE{self.order.id}'
    self.order.update_actual_price()
    self.order.save()
    super().save(*args, **kwargs)
    self.send_discord_notification()
    
  def get_details(self):
    return f"From {str(self.current_rank).upper()} {ten_romanize_division(self.current_division)} {'3' if self.current_marks == 0 else ('2' if self.current_marks == 1 else '1')} STAR To {str(self.desired_rank).upper()} {ten_romanize_division(self.desired_division)}"

  def __str__(self):
    return self.get_details()
  
  def get_rank_value(self, *args, **kwargs):
    return f"{self.current_rank.id},{self.current_division},{self.current_marks},{self.desired_rank.id},{self.desired_division},{self.order.duo_boosting},{self.order.select_booster},{self.order.turbo_boost},{self.select_champion},{self.order.streaming}"

