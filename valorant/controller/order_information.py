from django.shortcuts import get_object_or_404
import json
from valorant.models import *
from django.contrib.auth import get_user_model
from django.utils import timezone
from accounts.models import PromoCode

User = get_user_model()

division_names = ['','I','II','III']  
rank_names = ['UNRANK', 'IRON', 'BRONZE', 'SILVER', 'GOLD', 'PLATINUM', 'DIAMOND', 'ASCENDANT', 'IMMORTAL']

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
  booster_agents = data['booster_agents']

  server = data['server']
  promo_code = data['promo_code']

  duo_boosting_value = 0
  select_booster_value = 0
  turbo_boost_value = 0
  streaming_value = 0
  booster_agents_value = 0
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

  if turbo_boost:
    total_percent += 0.20
    boost_options.append('TURBO BOOSTING')
    turbo_boost_value = 1
  
  if streaming:
    total_percent += 0.15
    boost_options.append('STREAMING')
    streaming_value = 1

  if booster_agents:
    total_percent += 0.0
    boost_options.append('CHOOSE AGENTS')
    booster_agents_value = 1

  if promo_code != 'null':   
    try:
      promo_code_obj = PromoCode.objects.get(code=promo_code.lower())
      promo_code_amount = promo_code_obj.discount_amount
    except PromoCode.DoesNotExist:
      promo_code_amount = 0

  # Read data from JSON file
  with open('static/valorant/data/divisions_data.json', 'r') as file:
      division_price = json.load(file)
      flattened_data = [item for sublist in division_price for item in sublist]
      flattened_data.insert(0,0)
  ##
  with open('static/valorant/data/marks_data.json', 'r') as file:
      marks_data = json.load(file)
      marks_data.insert(0,[0,0,0,0,0,0])
  ##    
  start_division = ((current_rank-1) * 3) + current_division
  end_division = ((desired_rank-1) * 3)+ desired_division
  marks_price = marks_data[current_rank][marks]
  sublist = flattened_data[start_division:end_division ]
  total_sum = sum(sublist)
  price = total_sum - marks_price
  price += (price * total_percent)
  price -= price * (promo_code_amount/100)
  price = round(price, 2)

  if extend_order_id > 0:
    try:
      extend_order = BaseOrder.objects.get(id=extend_order_id)
      extend_order_price = extend_order.price
      price = round((price / (1 + total_percent)) - (extend_order_price / (1 + total_percent)), 2)
    except:
      pass

  booster_id = data['choose_booster']
  if booster_id > 0 :
    get_object_or_404(User,id=booster_id,is_booster=True)
  else:
    booster_id = 0

  invoice = f'valo-2-D-{current_rank}-{current_division}-{marks}-{desired_rank}-{desired_division}-{duo_boosting_value}-{select_booster_value}-{turbo_boost_value}-{streaming_value}-{booster_id}-{price}-{extend_order_id}-{server}-{booster_agents_value}-{timezone.now()}'
  print('Invoice', invoice)

  invoice_with_timestamp = str(invoice)
  boost_string = " WITH " + " AND ".join(boost_options) if boost_options else ""
  name = f'VALORANT, BOOSTING FROM {rank_names[current_rank]} {division_names[current_division]} MARKS {marks} TO {rank_names[desired_rank]} {division_names[desired_division]}{boost_string}'

  return({'name':name,'price':price,'invoice':invoice_with_timestamp})

def get_palcement_order_result_by_rank(data,extend_order_id):
  last_rank = data['last_rank']
  number_of_match = data['number_of_match']

  total_percent = 0
  
  duo_boosting = data['duo_boosting']
  select_booster = data['select_booster']
  turbo_boost = data['turbo_boost']
  streaming = data['streaming']
  booster_agents = data['booster_agents']

  server = data['server']
  promo_code = data['promo_code']

  duo_boosting_value = 0
  select_booster_value = 0
  turbo_boost_value = 0
  streaming_value = 0
  booster_agents_value = 0
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

  if turbo_boost:
    total_percent += 0.20
    boost_options.append('TURBO BOOSTING')
    turbo_boost_value = 1
  
  if streaming:
    total_percent += 0.15
    boost_options.append('STREAMING')
    streaming_value = 1

  if booster_agents:
    total_percent += 0.0
    boost_options.append('CHOOSE AGENTS')
    booster_agents_value = 1

  if promo_code != 'null':   
    try:
      promo_code_obj = PromoCode.objects.get(code=promo_code.lower())
      promo_code_amount = promo_code_obj.discount_amount
    except PromoCode.DoesNotExist:
      promo_code_amount = 0

  # Read data from JSON file
  with open('static/valorant/data/placements_data.json', 'r') as file:
    placement_data = json.load(file)
  ##    
  
  price = placement_data[last_rank] * number_of_match
  price += (price * total_percent)
  price -= price * (promo_code_amount/100)
  price = round(price, 2)

  if extend_order_id > 0:
    try:
      extend_order = BaseOrder.objects.get(id=extend_order_id)
      extend_order_price = extend_order.price
      price = round((price / (1 + total_percent)) - (extend_order_price / (1 + total_percent)), 2)
    except:
      pass

  booster_id = data['choose_booster']
  if booster_id > 0 :
    get_object_or_404(User,id=booster_id,is_booster=True)
  else:
    booster_id = 0

  invoice = f'valo-2-P-{last_rank}-{number_of_match}-none-none-none-{duo_boosting_value}-{select_booster_value}-{turbo_boost_value}-{streaming_value}-{booster_id}-{price}-{extend_order_id}-{server}-{booster_agents_value}-{timezone.now()}'
  print('Invoice', invoice)

  invoice_with_timestamp = str(invoice)
  boost_string = " WITH " + " AND ".join(boost_options) if boost_options else ""
  name = f'VALORANT, BOOSTING OF {number_of_match} Start With {rank_names[last_rank]}{boost_string}'

  return({'name':name,'price':price,'invoice':invoice_with_timestamp})