from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.utils import timezone
import json
from honorOfKings.models import *
from accounts.models import PromoCode

User = get_user_model()

division_names = ['','V','IV','III','II','I']
rank_names = ['UNRANK', 'BRONZE', 'SILVER', 'GOLD', 'PLATINUM', 'DIAMOND', 'KING']

def get_division_order_result_by_rank(data,extend_order_id):
  print('Data: ', data)
  # Division
  current_rank = data['current_rank']
  current_division = data['current_division']
  marks = data['marks']
  desired_rank = data['desired_rank']
  desired_division = data['desired_division']

  total_percent = 0

  duo_boosting = data['duo_boosting']
  select_booster = data['select_booster']
  turbo_boost = data['turbo_boost']
  streaming = data['streaming']

  server = data['server']
  promo_code = data['promo_code']

  duo_boosting_value = 0
  select_booster_value = 0
  turbo_boost_value = 0
  streaming_value = 0
  promo_code_amount = 0

  boost_options = []

  if duo_boosting:
    total_percent += 0.65
    boost_options.append('DUO BOOSTING')
    duo_boosting_value = 1

  if select_booster:
    total_percent += 0.10
    boost_options.append('SELECT BOOSTING')
    select_booster_value = 1
  
  if streaming:
    total_percent += 0.15
    boost_options.append('STREAMING')
    streaming_value = 1

  if turbo_boost:
    total_percent += 0.20
    boost_options.append('TURBO BOOSTING')
    turbo_boost_value = 1

  if promo_code != 'null':   
    try:
      promo_code_obj = PromoCode.objects.get(code=promo_code.lower())
      promo_code_amount = promo_code_obj.discount_amount
    except PromoCode.DoesNotExist:
      promo_code_amount = 0

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
  start_division = ((current_rank-1) * 5) + current_division
  end_division = ((desired_rank-1) * 5) + desired_division
  marks_price = marks_data[current_rank][marks]
  sublist = flattened_data[start_division:end_division ]
  total_sum = sum(sublist)
  price = total_sum - marks_price
  price += (price * total_percent)
  price -= price * (promo_code_amount/100)
  price = round(price, 2)
  print('Price', price)

  if extend_order_id > 0:
    try:
      extend_order = BaseOrder.objects.get(id=extend_order_id)
      extend_order_price = extend_order.price
      price = round((price) - (extend_order_price), 2)
    except:
      pass

  booster_id = data['choose_booster']
  if booster_id > 0 :
    get_object_or_404(User,id=booster_id,is_booster=True)
  else:
    booster_id = 0

  invoice = f'HOK-11-D-{current_rank}-{current_division}-{marks}-{desired_rank}-{desired_division}-{duo_boosting_value}-{select_booster_value}-{turbo_boost_value}-{streaming_value}-{booster_id}-{extend_order_id}-{server}-{price}-0-{promo_code}-0-0'
  print('Invoice', invoice)

  invoice_with_timestamp = str(invoice)
  boost_string = " WITH " + " AND ".join(boost_options) if boost_options else ""
  name = f'HOK, BOOSTING FROM {rank_names[current_rank]} {division_names[current_division]} MARKS {marks} TO {rank_names[desired_rank]} {division_names[desired_division]}{boost_string}'

  return({'name':name,'price':price,'invoice':invoice_with_timestamp})