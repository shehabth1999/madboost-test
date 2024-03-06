from django.db import models
from accounts.models import BaseOrder, Wallet
from accounts.templatetags.custom_filters import romanize_division_original
import requests
import json

# Create your models here.
class ValorantRank(models.Model):
  rank_name = models.CharField(max_length=25)
  rank_image = models.ImageField(upload_to='valorant/images/', blank=True, null=True)

  def __str__(self):
    return self.rank_name
    
  def get_image_url(self):
    return f"/media/{self.rank_image}"
  
class ValorantTier(models.Model):
  rank = models.OneToOneField('ValorantRank', related_name='tier', on_delete=models.CASCADE)
  from_I_to_II = models.FloatField(default=0)
  from_II_to_III = models.FloatField(default=0)
  from_III_to_I_next = models.FloatField(default=0)

  def __str__(self):
    return f"Tiers for {self.rank.rank_name}"

class ValorantMark(models.Model):
  rank = models.OneToOneField('ValorantRank', related_name='mark', on_delete=models.CASCADE)
  marks_0_20 = models.FloatField(default=0)
  marks_21_40 = models.FloatField(default=0)
  marks_41_60 = models.FloatField(default=0)
  marks_61_80 = models.FloatField(default=0)
  marks_81_100 = models.FloatField(default=0)
  

  def __str__(self):
    return f"{self.rank} -> Marks 0-20 : {self.marks_0_20}, Marks 21_40 : {self.marks_21_40}, Marks 41_60 : {self.marks_41_60}, Marks 61_80 : {self.marks_61_80}, Marks 81_100 : {self.marks_81_100}"
  
class ValorantPlacement(models.Model):
  rank_name = models.CharField(max_length=25)
  rank_image = models.ImageField(upload_to='valorant/images/', blank=True, null=True)
  price = models.FloatField()

  def __str__(self):
    return self.rank_name
  
  def get_image_url(self):
    return f"/media/{self.rank_image}"
  
class ValorantDivisionOrder(models.Model):
  DIVISION_CHOICES = [
    (1, 'I'),
    (2, 'II'),
    (3, 'III'),
  ]
  MARKS_CHOISES = [
    (0, '0-20'),
    (1 , '21-40'),
    (2, '41-60'),
    (3, '61-80'),
    (4, '81-100')
  ]
  order = models.OneToOneField(BaseOrder, on_delete=models.CASCADE, primary_key=True, default=None, related_name='valorant_division_order')
  current_rank = models.ForeignKey(ValorantRank, on_delete=models.CASCADE, default=None, related_name='current_rank',blank=True, null=True)
  reached_rank = models.ForeignKey(ValorantRank, on_delete=models.CASCADE, default=None, related_name='reached_rank',blank=True, null=True)
  desired_rank = models.ForeignKey(ValorantRank, on_delete=models.CASCADE, default=None, related_name='desired_rank',blank=True, null=True)
  current_division = models.IntegerField(choices=DIVISION_CHOICES,blank=True, null=True)
  reached_division = models.IntegerField(choices=DIVISION_CHOICES,blank=True, null=True)
  desired_division = models.IntegerField(choices=DIVISION_CHOICES,blank=True, null=True)
  current_marks = models.IntegerField(choices=MARKS_CHOISES,blank=True, null=True)
  reached_marks = models.IntegerField(choices=MARKS_CHOISES,blank=True, null=True)
  created_at = models.DateTimeField(auto_now_add =True)
  choose_agents = models.BooleanField(default=True, blank=True, null=True)

  def send_discord_notification(self):
    if self.order.status == 'Extend':
      return print('Extend Order')
    discord_webhook_url = 'https://discord.com/api/webhooks/1190613917853032554/ox-bqYupSInRiv3x41Fgj0Nh6gKZjbfkdnJvX1vIokc68xqQqyXmg1hEz6ZtrqGONbaR'
    current_time = self.created_at.strftime("%Y-%m-%d %H:%M:%S")
    embed = {
      "title": "Vlorant",
      "description": (
        f"**Order ID:** {self.order.name}\n"
        f" From {str(self.current_rank).upper()} {romanize_division_original(self.current_division)} Points {self.current_marks} "
        f" {str(self.current_rank).upper()} {romanize_division_original(self.current_division)} Points {self.current_marks} To {str(self.desired_rank).upper()} {romanize_division_original(self.desired_division)} server us" # change server next
      ),
      "color": 0xff9999,  # Hex color code for a Discord color
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
    self.order.game_id = 2
    self.order.game_type = 'D'
    self.order.details = self.get_details()
    if not self.order.name:
      self.order.name = f'Valo{self.order.id}'
    self.order.update_actual_price()
    self.order.save()
    super().save(*args, **kwargs)
    self.send_discord_notification()
    
  def get_details(self):
    return f"From {str(self.current_rank).upper()} {romanize_division_original(self.current_division)} {'0-20' if self.current_marks == 0 else ('21-40' if self.current_marks == 1 else ('41-60' if self.current_marks == 2 else ('61-80' if self.current_marks == 3 else '81-100')))} RR To {str(self.desired_rank).upper()} {romanize_division_original(self.desired_division)}"



  def __str__(self):
    return self.get_details()
  
  def get_rank_value(self, *args, **kwargs):
    return f"{self.current_rank.id},{self.current_division},{self.current_marks},{self.desired_rank.id},{self.desired_division},{self.order.duo_boosting},{False},{self.order.turbo_boost},{self.order.streaming },{self.choose_agents}"
  
  def get_rank_value(self, *args, **kwargs):
    return f"{self.current_rank.id},{self.current_division},{self.current_marks},{self.desired_rank.id},{self.desired_division},{self.order.duo_boosting},{self.order.select_booster},{self.order.turbo_boost},{self.order.streaming},{self.booster_champions}"
    

  def get_order_price(self):
    # Read data from JSON file
    with open('static/valorant/data/divisions_data.json', 'r') as file:
      division_price = json.load(file)
      flattened_data = [item for sublist in division_price for item in sublist]
      flattened_data.insert(0,0)
    ##
    with open('static/valorant/data/marks_data.json', 'r') as file:
      marks_data = json.load(file)
      marks_data.insert(0,[0,0,0,0,0])
    ##   
          
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
    marks_price = marks_data[current_rank][current_marks]
    marks_price_reached = 0
    marks_price_reached = marks_data[reached_rank][reached_marks]

    sublist = flattened_data[start_division:end_division]


    total_sum = sum(sublist)    


    custom_price = total_sum - marks_price + marks_price_reached
    
    custom_price += (custom_price * total_percent)
    custom_price -= custom_price * (promo_code_amount/100)

    ##############################################################

    actual_price = self.order.actual_price
    main_price = self.order.price

    percent = round(actual_price / (main_price/100))

    booster_price = custom_price * (percent/100)

    percent_for_view = round((booster_price/actual_price)* 100)
    if percent_for_view > 100:
      percent_for_view = 100

    if booster_price > actual_price:
      booster_price = actual_price


    return {"booster_price":booster_price, 'percent_for_view':percent_for_view}
    
class ValorantPlacementOrder(models.Model):
  order = models.OneToOneField(BaseOrder, on_delete=models.CASCADE, primary_key=True, default=None, related_name='valorant_placement_order')
  last_rank = models.ForeignKey(ValorantPlacement, on_delete=models.CASCADE, default=None, related_name='last_rank')
  number_of_match = models.IntegerField(default=5)

  choose_agents = models.BooleanField(default=False, blank=True, null=True)

  def save_with_processing(self, *args, **kwargs):
    self.order.game_id = 2
    self.order.game_type = 'P'
    self.order.details = self.get_details()
    if not self.order.name:
      self.order.name = f'Valo{self.order.id}'
    self.order.update_actual_price()
    self.order.save()
    super().save(*args, **kwargs)

  def get_details(self):
    return f"Boosting of {self.number_of_match} Placement Games With Rank {self.last_rank}"

  def __str__(self):
    return self.get_details()