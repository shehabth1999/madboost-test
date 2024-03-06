from django.db import models
from accounts.models import BaseOrder, Wallet
from accounts.templatetags.custom_filters import five_romanize_division
import json

# Create your models here.
class HonorOfKingsRank(models.Model):
  rank_name = models.CharField(max_length=25)
  rank_image = models.ImageField(upload_to='hok/images/', blank=True, null=True)

  def __str__(self):
    return self.rank_name
    
  def get_image_url(self):
    return f"/media/{self.rank_image}"
  
class HonorOfKingsTier(models.Model):
  rank = models.OneToOneField('HonorOfKingsRank', related_name='tier', on_delete=models.CASCADE)
  from_V_to_IV = models.FloatField(default=0)
  from_IV_to_III = models.FloatField(default=0)
  from_III_to_II = models.FloatField(default=0)
  from_II_to_I = models.FloatField(default=0)
  from_I_to_IV_next = models.FloatField(default=0)

  def __str__(self):
    return f"Tiers for {self.rank.rank_name}"

class HonorOfKingsMark(models.Model):
  rank = models.OneToOneField('HonorOfKingsRank', related_name='mark', on_delete=models.CASCADE)
  star_1 = models.FloatField(default=0)
  star_2 = models.FloatField(default=0)
  star_3 = models.FloatField(default=0)

  def __str__(self):
    return f"{self.rank} -> Star 1: {self.star_1}, Star 2: {self.star_2}, Star 3: {self.star_3}"
  
class HonorOfKingsDivisionOrder(models.Model):
  DIVISION_CHOICES = [
    (1, 'V'),
    (2, 'IV'),
    (3, 'III'),
    (4, 'II'),
    (5, 'I'),
  ]
  MARKS_CHOISES = [
    (0, '0 Stars'),
    (1, '1 Stars'),
    (2, '2 Stars'),
    (3, '3 Stars'),
  ]
  order = models.OneToOneField(BaseOrder, on_delete=models.CASCADE, primary_key=True, default=None, related_name='hok_division_order')
  current_rank = models.ForeignKey(HonorOfKingsRank, on_delete=models.CASCADE, default=None, related_name='current_rank',blank=True, null=True)
  reached_rank = models.ForeignKey(HonorOfKingsRank, on_delete=models.CASCADE, default=None, related_name='reached_rank',blank=True, null=True)
  desired_rank = models.ForeignKey(HonorOfKingsRank, on_delete=models.CASCADE, default=None, related_name='desired_rank',blank=True, null=True)
  current_division = models.IntegerField(choices=DIVISION_CHOICES,blank=True, null=True)
  reached_division = models.IntegerField(choices=DIVISION_CHOICES,blank=True, null=True)
  desired_division = models.IntegerField(choices=DIVISION_CHOICES,blank=True, null=True)
  current_marks = models.IntegerField(choices=MARKS_CHOISES,blank=True, null=True)
  reached_marks = models.IntegerField(choices=MARKS_CHOISES,blank=True, null=True)
  created_at = models.DateTimeField(auto_now_add =True)

  def save_with_processing(self, *args, **kwargs):
    self.order.game_id = 11
    self.order.game_type = 'D'
    self.order.details = self.get_details()
    if not self.order.name:
      self.order.name = f'HOK{self.order.id}'
    self.order.update_actual_price()
    self.order.save()
    super().save(*args, **kwargs)
    # self.send_discord_notification()
    
  def get_details(self):
    return f"From {str(self.current_rank).upper()} {five_romanize_division(self.current_division)} {self.current_marks} Stars To {str(self.desired_rank).upper()} {five_romanize_division(self.desired_division)}"

  def __str__(self):
    return self.get_details()
  
  def get_rank_value(self, *args, **kwargs):
    return f"{self.current_rank.id},{self.current_division},{self.current_marks},{self.desired_rank.id},{self.desired_division},{self.order.duo_boosting},{self.order.select_booster},{self.order.turbo_boost},{self.order.streaming}"
  
  def get_rank_value(self, *args, **kwargs):
    return f"{self.current_rank.id},{self.current_division},{self.current_marks},{self.desired_rank.id},{self.desired_division},{self.order.duo_boosting},{self.order.select_booster},{self.order.turbo_boost},{self.order.streaming},{self.booster_champions}"
    

  def get_order_price(self):
    # Read data from JSON file
    with open('static/hok/data/divisions_data.json', 'r') as file:
      division_price = json.load(file)
      flattened_data = [item for sublist in division_price for item in sublist]
      flattened_data.insert(0,0)
    ##
    with open('static/hok/data/marks_data.json', 'r') as file:
      marks_data = json.load(file)
      marks_data.insert(0,[0,0,0,0])
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

    start_division = ((current_rank-1)*5) + current_division
    end_division = ((reached_rank-1)*5)+ reached_division
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

    print(percent)

    booster_price = custom_price * (percent/100)

    percent_for_view = round((booster_price/actual_price)* 100)
    if percent_for_view > 100:
      percent_for_view = 100

    if booster_price > actual_price:
      booster_price = actual_price


    return {"booster_price":booster_price, 'percent_for_view':percent_for_view}