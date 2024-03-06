from django.shortcuts import get_object_or_404
import json
from tft.models import *
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

division_names = ['','IV','III','II','I']  
rank_names = ['UNRANK', 'IRON', 'BRONZE', 'SILVER', 'GOLD', 'PLATINUM', 'EMERALD', 'DIAMOND', 'MASTER']

def get_division_order_result_by_rank(data,extend_order_id):
  print('Data: ', data)
  # Division
  current_rank = data['current_rank']
  current_division = data['current_division']
  marks = data['marks']
  desired_rank = data['desired_rank']
  desired_division = data['desired_division']

  total_percent = 0
  select_booster = data['select_booster']
  streaming = data['streaming']
  speed_up_boost = data['speed_up_boost']

  select_booster_value = 0
  streaming_value = 0
  speed_up_boost_value = 0

  boost_options = []

  if select_booster:
    total_percent += 0.05
    boost_options.append('SELECT BOOSTING')
    select_booster_value = 1
  
  if streaming:
    total_percent += 0.15
    boost_options.append('STREAMING')
    streaming_value = 1

  if speed_up_boost:
    total_percent += 0.25
    boost_options.append('SPEED UP BOOST')
    speed_up_boost_value = 1

  # Read data from JSON file
  with open('static/tft/data/divisions_data.json', 'r') as file:
    division_price = json.load(file)
    flattened_data = [item for sublist in division_price for item in sublist]
    flattened_data.insert(0,0)
  ##
  with open('static/tft/data/marks_data.json', 'r') as file:
    marks_data = json.load(file)
    marks_data.insert(0,[0,0,0,0,0,0])
  ##    
  start_division = ((current_rank-1) * 4) + current_division
  end_division = ((desired_rank-1) * 4)+ desired_division
  marks_price = marks_data[current_rank][marks]
  sublist = flattened_data[start_division:end_division ]
  total_sum = sum(sublist)
  price = total_sum - marks_price
  price += (price * total_percent)
  price = round(price, 2)
  print('Price', price)

  if extend_order_id > 0:
    try:
      extend_order = BaseOrder.objects.get(id=extend_order_id)
      extend_order_price = extend_order.price
      price = round((price - extend_order_price), 2)
      print('Price', price)
    except:
      pass

  booster_id = data['choose_booster']
  if booster_id > 0 :
    get_object_or_404(User,id=booster_id,is_booster=True)
  else:
    booster_id = 0

  invoice = f'tft-5-D-{current_rank}-{current_division}-{marks}-{desired_rank}-{desired_division}-0-{select_booster_value}-0-{streaming_value}-{booster_id}-{price}-{extend_order_id}-{timezone.now()}-?-{speed_up_boost_value}'
  print('Invoice', invoice)

  invoice_with_timestamp = str(invoice)
  boost_string = " WITH " + " AND ".join(boost_options) if boost_options else ""
  name = f'TFT, BOOSTING FROM {rank_names[current_rank]} {division_names[current_division]} MARKS {marks} TO {rank_names[desired_rank]} {division_names[desired_division]}{boost_string}'

  return({'name':name,'price':price,'invoice':invoice_with_timestamp})

def get_palcement_order_result_by_rank(data,extend_order_id):
  last_rank = data['last_rank']
  number_of_match = data['number_of_match']

  total_percent = 0
  select_booster = data['select_booster']
  streaming = data['streaming']
  speed_up_boost = data['speed_up_boost']

  select_booster_value = 0
  streaming_value = 0
  speed_up_boost_value = 0

  boost_options = []

  if select_booster:
    total_percent += 0.05
    boost_options.append('SELECT BOOSTING')
    select_booster_value = 1
  
  if streaming:
    total_percent += 0.15
    boost_options.append('STREAMING')
    streaming_value = 1

  if speed_up_boost:
    total_percent += 0.25
    boost_options.append('SPEED UP BOOST')
    speed_up_boost_value = 1

  # Read data from JSON file
  with open('static/tft/data/placements_data.json', 'r') as file:
    placement_data = json.load(file)
  ##    
  
  price = placement_data[last_rank] * number_of_match
  price += (price * total_percent)
  price = round(price, 2)
  print('Placement Price: ', price)

  if extend_order_id > 0:
    try:
      extend_order = BaseOrder.objects.get(id=extend_order_id)
      extend_order_price = extend_order.price
      price = round((price - extend_order_price), 2)
      print('Price', price)
    except:
      pass

  booster_id = data['choose_booster']
  if booster_id > 0 :
    get_object_or_404(User,id=booster_id,is_booster=True)
  else:
    booster_id = 0

  invoice = f'tft-5-P-{last_rank}-{number_of_match}-?-?-?-0-{select_booster_value}-0-{streaming_value}-{booster_id}-{price}-{extend_order_id}-{timezone.now()}-?-{speed_up_boost_value}'
  print('Invoice', invoice)

  invoice_with_timestamp = str(invoice)
  boost_string = " WITH " + " AND ".join(boost_options) if boost_options else ""
  name = f'TFT, BOOSTING OF {number_of_match} Start With {rank_names[last_rank]}{boost_string}'

  return({'name':name,'price':price,'invoice':invoice_with_timestamp})