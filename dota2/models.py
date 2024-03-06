from django.db import models
from accounts.models import BaseOrder
import requests
from django.core.exceptions import ValidationError

class Dota2Rank(models.Model):
  rank_name = models.CharField(max_length=25)
  rank_image = models.ImageField(upload_to='dota2/images/', blank=True, null=True)
  start_RP = models.IntegerField()
  end_RP = models.IntegerField()

  def __str__(self):
    return self.rank_name
    
  def get_image_url(self):
    return f"/media/{self.rank_image}"

class Dota2_50_MMR_Price(models.Model):
  price = models.IntegerField(default=1)

  def __str__(self):
    return f"Price for 50 RPs is {self.price}"
  
  
class Dota2RankBoostOrder(models.Model):
  ROLE_CHOISES = (
        (1, 'Core'),
        (2, 'Support'),
  )
  order = models.OneToOneField(BaseOrder, on_delete=models.CASCADE, primary_key=True, default=None, related_name='dota2_division_order')
  current_rank = models.ForeignKey(Dota2Rank, on_delete=models.CASCADE, default=None, related_name='dota2_current_rank')
  reached_rank = models.ForeignKey(Dota2Rank, on_delete=models.CASCADE, default=None, related_name='dota2_reached_rank')
  desired_rank = models.ForeignKey(Dota2Rank, on_delete=models.CASCADE, default=None, related_name='dota2_desired_rank')
  
  current_division = models.IntegerField(default=0)
  reached_division = models.IntegerField(default=0)
  desired_division = models.IntegerField(default=0)

  current_marks = models.PositiveSmallIntegerField(blank=True, null=True, default= 0)
  reached_marks = models.PositiveSmallIntegerField(blank=True, null=True, default= 0)

  select_champion = models.BooleanField(default=True, blank=True, null=True)
  role = models.PositiveSmallIntegerField(choices=ROLE_CHOISES, null=True, blank=True)

  created_at = models.DateTimeField(auto_now_add =True)


  def validate_divition(self):
    if not (self.current_division > 0 and self.current_division <= 7000):
        raise ValidationError("Current division must be between 0 and 7000.")
        
  def send_discord_notification(self):
    if self.order.status == 'Extend':
      return print('Extend Order')
    discord_webhook_url = 'https://discordapp.com/api/webhooks/1209759469806821396/Sw69hAULnlb4XIEIclX_Ag-xCdinblnLcpr01UXtJDM2STpTw2hv8UqyD29qY2H01uXX'
    current_time = self.created_at.strftime("%Y-%m-%d %H:%M:%S")
    embed = {
      "title": "Dota 2",
      "description": (
        f"**Order ID:** {self.order.name}\n"
        f" From {self.current_division} RP"
        f" To {self.desired_division} RP server {self.order.customer_server}" # change server next
      ),
      "color": 0xFFA500,  # Hex color code for a Discord color
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
    self.validate_divition()
    # self.order.game_id = 11
    # self.order.game_name = 'dota2'
    self.order.game_type = 'A'
    self.order.details = self.get_details()
    if not self.order.name:
      self.order.name = f'dota2{self.order.id}'
    self.order.update_actual_price()
    self.order.save()
    super().save(*args, **kwargs)
    self.send_discord_notification()

  def get_details(self):
      return f"From {self.current_division} RP To {self.desired_division}"
    
  def __str__(self):
    return f"Boosting From {self.current_division} RP To {self.desired_division}"

  def get_rank_value(self, *args, **kwargs):
    return f"{self.current_division},{self.desired_division},{self.order.duo_boosting},{self.order.select_booster},{self.order.turbo_boost},{self.order.streaming },{self.select_champion}"
