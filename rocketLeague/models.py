from django.db import models
from accounts.models import BaseOrder, Wallet
from accounts.templatetags.custom_filters import romanize_division_original, romanize_division
import requests
import json

# Create your models here.
class RocketLeagueRank(models.Model):
  rank_name = models.CharField(max_length=25)
  rank_image = models.ImageField(upload_to='rocketLeague/images/', blank=True, null=True)

  def __str__(self):
    return self.rank_name
    
  def get_image_url(self):
    return f"/media/{self.rank_image}"
  
class RocketLeagueDivision(models.Model):
  rank = models.OneToOneField('RocketLeagueRank', related_name='tier', on_delete=models.CASCADE)
  from_I_to_II = models.FloatField(default=0)
  from_II_to_III = models.FloatField(default=0)
  from_III_to_I_next = models.FloatField(default=0)

  def __str__(self):
    return f"Tiers for {self.rank.rank_name}"
  
class RocketLeaguePlacement(models.Model):
  rank_name = models.CharField(max_length=25)
  rank_image = models.ImageField(upload_to='rocketLeague/images/', blank=True, null=True)
  price = models.FloatField()

  def __str__(self):
    return f'{self.rank_name} - {self.price}$'
  
  def get_image_url(self):
    return f"/media/{self.rank_image}"
  
class RocketLeagueSeasonal(models.Model):
  rank_name = models.CharField(max_length=25)
  rank_image = models.ImageField(upload_to='rocketLeague/images/', blank=True, null=True)
  price = models.FloatField()

  def __str__(self):
    return f'{self.rank_name} - {self.price}$'
  
  def get_image_url(self):
    return f"/media/{self.rank_image}"
  
class RocketLeagueTournament(models.Model):
  rank_name = models.CharField(max_length=25)
  rank_image = models.ImageField(upload_to='rocketLeague/images/', blank=True, null=True)
  price = models.FloatField()

  def __str__(self):
    return f'{self.rank_name} - {self.price}$'
  
  def get_image_url(self):
    return f"/media/{self.rank_image}"
  
class RocketLeagueDivisionOrder(models.Model):
  DIVISION_CHOICES = [
    (1, 'I'),
    (2, 'II'),
    (3, 'III'),
  ]
  RANKED_TYPE = [
    (1, "1 vs 1 Ranked"),
    (2, "2 vs 2 Ranked"),
    (3, "3 vs 3 Ranked"),
  ]
  order = models.OneToOneField(BaseOrder, on_delete=models.CASCADE, primary_key=True, default=None, related_name='rocketLeague_division_order')
  ranked_type = models.IntegerField(choices=RANKED_TYPE,blank=True, null=True)
  current_rank = models.ForeignKey(RocketLeagueRank, on_delete=models.CASCADE, default=None, related_name='current_rank',blank=True, null=True)
  reached_rank = models.ForeignKey(RocketLeagueRank, on_delete=models.CASCADE, default=None, related_name='reached_rank',blank=True, null=True)
  desired_rank = models.ForeignKey(RocketLeagueRank, on_delete=models.CASCADE, default=None, related_name='desired_rank',blank=True, null=True)
  current_division = models.IntegerField(choices=DIVISION_CHOICES,blank=True, null=True)
  reached_division = models.IntegerField(choices=DIVISION_CHOICES,blank=True, null=True)
  desired_division = models.IntegerField(choices=DIVISION_CHOICES,blank=True, null=True)
  current_marks = models.IntegerField(default=0,blank=True, null=True)
  reached_marks = models.IntegerField(default=0,blank=True, null=True)
  created_at = models.DateTimeField(auto_now_add =True)
  
  def send_discord_notification(self):
    if self.order.status == 'Extend':
        return print('Extend Order')
    discord_webhook_url = 'https://discordapp.com/api/webhooks/1209761850678583346/X6pCjDZ4C65kbbshT9grGbgfVCf4rAYWg6isSN8qmJuIjZG7N4CQtXp0c3GKKzoJFbFf'
    current_time = self.created_at.strftime("%Y-%m-%d %H:%M:%S")
    embed = {
        "title": "Rocket League",
        "description": (
            f"**Order ID:** {self.order.name}\n"
            f" From {str(self.current_rank).upper()} {romanize_division(self.current_division)} "
            f" To {str(self.desired_rank).upper()} {romanize_division(self.desired_division)}\n {self.get_ranked_type_display()} server USA" # change server next
        ),
        "color": 0xff8c00,  # Hex color code for a Discord blue color
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
    self.order.game_id = 9
    self.order.game_name = 'rocketLeague'
    self.order.game_type = 'D'
    self.order.details = self.get_details()
    if not self.order.name:
      self.order.name = f'RL{self.order.id}'
    self.order.update_actual_price()
    self.order.save()
    super().save(*args, **kwargs)
    self.send_discord_notification()

    
  def get_details(self):
    return f"From {str(self.current_rank).upper()} {romanize_division_original(self.current_division)} To {str(self.desired_rank).upper()} {romanize_division_original(self.desired_division)}"

  def __str__(self):
    return self.get_details()
  
  def get_rank_value(self, *args, **kwargs):
    return f"{self.current_rank.id},{self.current_division},{self.ranked_type},{self.desired_rank.id},{self.desired_division},{self.order.duo_boosting},{False},{self.order.turbo_boost},{self.order.streaming }"
  
  def get_order_price(self):
    # Read data from JSON file
    with open('static/rocketLeague/data/divisions_data.json', 'r') as file:
      division_price = json.load(file)
      flattened_data = [item for sublist in division_price for item in sublist]
      flattened_data.insert(0,0)  
          
    promo_code_amount = self.order.promo_code
    if not promo_code_amount:
      promo_code_amount = 0

    current_rank = self.current_rank.id
    reached_rank = self.reached_rank.id

    current_division = self.current_division
    reached_division = self.reached_division

    current_marks = self.current_marks
    reached_marks = self.reached_marks

    total_percent = 0

    if self.order.duo_boosting:
      total_percent += 0.65

    if self.order.select_booster:
      total_percent += 0.10

    if self.order.turbo_boost:
      total_percent += 0.20

    if self.order.streaming:
      total_percent += 0.15

    start_division = ((current_rank-1)*3) + current_division
    end_division = ((reached_rank-1)*3)+ reached_division

    sublist = flattened_data[start_division:end_division]


    total_sum = sum(sublist)    


    custom_price = total_sum
    
    custom_price += (custom_price * total_percent)
    custom_price -= custom_price * (promo_code_amount/100)

    ##############################################################

    actual_price = self.order.actual_price
    main_price = self.order.price

    percent = round(actual_price / (main_price/100))

    print(percent)

    booster_price = custom_price * (percent/100)

    percent_for_view = round((booster_price/actual_price)* 100)
    if percent_for_view > 100:
      percent_for_view = 100

    if booster_price > actual_price:
      booster_price = actual_price


    return {"booster_price":booster_price, 'percent_for_view':percent_for_view}

class RocketLeaguePlacementOrder(models.Model):
  order = models.OneToOneField(BaseOrder, on_delete=models.CASCADE, primary_key=True, default=None, related_name='rocketLeague_placement_order')
  last_rank = models.ForeignKey(RocketLeaguePlacement, on_delete=models.CASCADE, default=None, related_name='last_rank')
  number_of_match = models.IntegerField(default=10)

  def send_discord_notification(self):
    if self.order.status == 'Extend':
        return print('Extend Order')
    discord_webhook_url = 'https://discordapp.com/api/webhooks/1209761850678583346/X6pCjDZ4C65kbbshT9grGbgfVCf4rAYWg6isSN8qmJuIjZG7N4CQtXp0c3GKKzoJFbFf'
    current_time = self.created_at.strftime("%Y-%m-%d %H:%M:%S")
    embed = {
        "title": "Rift",
        "description": (
            f"**Order ID:** {self.order.name}\n"
            f"Placement {self.number_of_match} matchs with last_rank {self.last_rank}"
        ),
        "color": 0xff8c00,  # Hex color code for a Discord blue color
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
    self.order.game_id = 9
    self.order.game_name = 'rocketLeague'
    self.order.game_type = 'P'
    self.order.details = self.get_details()
    if not self.order.name:
      self.order.name = f'RL{self.order.id}'
    self.order.update_actual_price()
    self.order.save()
    super().save(*args, **kwargs)
    self.send_discord_notification()


  def get_details(self):
    return f"Boosting of {self.number_of_match} Placement Games With Rank {self.last_rank}"

  def __str__(self):
    return self.get_details()
  
class RocketLeagueSeasonalOrder(models.Model):
  order = models.OneToOneField(BaseOrder, on_delete=models.CASCADE, primary_key=True, default=None, related_name='rocketLeague_seasonal_order')
  current_rank = models.ForeignKey(RocketLeagueSeasonal, on_delete=models.CASCADE, default=None, related_name='current_rank')
  number_of_wins = models.IntegerField(default=5)

  def save_with_processing(self, *args, **kwargs):
    self.order.game_id = 9
    self.order.game_name = 'rocketLeague'
    self.order.game_type = 'S'
    self.order.details = self.get_details()
    if not self.order.name:
      self.order.name = f'RL{self.order.id}'
    self.order.update_actual_price()
    self.order.save()
    super().save(*args, **kwargs)

  def get_details(self):
    return f"Seasonal Reward Boosting by {self.number_of_wins} Wins With Rank {self.current_rank}"

  def __str__(self):
    return self.get_details()
  
class RocketLeagueTournamentOrder(models.Model):
  order = models.OneToOneField(BaseOrder, on_delete=models.CASCADE, primary_key=True, default=None, related_name='rocketLeague_ournament_order')
  current_league = models.ForeignKey(RocketLeagueTournament, on_delete=models.CASCADE, default=None, related_name='current_league')

  def save_with_processing(self, *args, **kwargs):
    self.order.game_id = 9
    self.order.game_name = 'rocketLeague'
    self.order.game_type = 'T'
    self.order.details = self.get_details()
    if not self.order.name:
      self.order.name = f'RL{self.order.id}'
    self.order.update_actual_price()
    self.order.save()
    super().save(*args, **kwargs)

  def get_details(self):
    return f"{self.current_league} League Tournament Win"

  def __str__(self):
    return self.get_details()