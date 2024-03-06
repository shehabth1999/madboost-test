from django.shortcuts import get_object_or_404
import json
from django.utils import timezone
from dota2.models import Dota2_50_MMR_Price, BaseOrder
from django.contrib.auth import get_user_model
User = get_user_model()

# Ranking System
# Herald — 0-769 MMR.
# Guardian — 770-1539 MMR.
# Crusader — 1540-2309 MMR.
# Archon — 2310-3079 MMR.
# Legend — 3080-3849 MMR.
# Ancient — 3850-4619 MMR.
# Divine — 4620-5420 MMR.
# Immortal — ∽6000+ MMR.

rank_names = ['UNRANK', 'HERALD', 'GUARDIAN', 'CRUSADER', 'ARCHON', 'LEGEND', 'ANCIENT', 'DIVINE', 'IMMORTAL']
role_names = ['NoRole', 'Core', 'Support']


def get_rank_boost_order_result_by_rank(data,extend_order_id):
  # Division
  current_division = data['current_division']
  desired_division = data['desired_division']

  total_percent = 0
  duo_boosting = data['duo_boosting']
  select_booster = data['select_booster']
  turbo_boost = data['turbo_boost']
  streaming = data['streaming']
  select_champion = data['select_champion']
  role_data = data['role']
  server = data['server']
  promo_code = data['promo_code']

  duo_boosting_value = 0
  select_booster_value = 0
  turbo_boost_value = 0
  streaming_value = 0
  select_champion_value = 0

  boost_options = []

  if duo_boosting:
    total_percent += 0.65
    boost_options.append('DUO BOOSTING')
    duo_boosting_value = 1

  if select_booster:
    total_percent += 0.05
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

  if select_champion:
    total_percent += 0.0
    boost_options.append('CHOOSE AGENTS')
    select_champion_value = 1
      
  dota_50_MMR_Price = Dota2_50_MMR_Price.objects.all().first().price
  total_sum = (desired_division - current_division) * (dota_50_MMR_Price * 50)
  price = total_sum + (total_sum * total_percent)
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

  if current_division >= 0 and current_division <= 769 :
    current_rank = 1 # Herald 
  elif current_division >= 770 and current_division <= 1539:
    current_rank = 2 # Guardian 
  elif current_division >= 1540 and current_division <= 2309:
    current_rank = 3 # Crusader 
  elif current_division >= 2310 and current_division <= 3079:
    current_rank = 4 # Archon 
  elif current_division >= 3080 and current_division <= 3849:
    current_rank = 5 # Legend 
  elif current_division >= 3850 and current_division <= 4619:
    current_rank = 6 # Ancient 
  elif current_division >= 4620 and current_division <= 5420:
    current_rank = 7 # Divine 
  elif current_division >= 5421:
    current_rank = 8 # Immortal 
  else:
    current_rank = rank_names[0]
  
  if desired_division >= 0 and desired_division <= 769 :
    desired_rank = 1 # Herald 
  elif desired_division >= 770 and desired_division <= 1539:
    desired_rank = 2 # Guardian 
  elif desired_division >= 1540 and desired_division <= 2309:
    desired_rank = 3 # Crusader 
  elif desired_division >= 2310 and desired_division <= 3079:
    desired_rank = 4 # Archon 
  elif desired_division >= 3080 and desired_division <= 3849:
    desired_rank = 5 # Legend 
  elif desired_division >= 3850 and desired_division <= 4619:
    desired_rank = 6 # Ancient 
  elif desired_division >= 4620 and desired_division <= 5420:
    desired_rank = 7 # Divine 
  elif desired_division >= 5421:
    desired_rank = 8 # Immortal 
  else:
    desired_rank = rank_names[0]
  
  invoice = f'WOW-6-A-{current_rank}-{current_division}-0-{desired_rank}-{desired_division}-{duo_boosting_value}-{select_booster_value}-{turbo_boost_value}-{streaming_value}-{booster_id}-{extend_order_id}-{server}-{price}-{select_champion_value}-{promo_code}-{role_data}-0'
  invoice_with_timestamp = str(invoice)
  boost_string = " WITH " + " AND ".join(boost_options) if boost_options else ""
  name = f'WOW, BOOSTING FROM {rank_names[current_rank]} {current_division} TO {rank_names[desired_rank]} {desired_division}{boost_string} ROLE: {role_names[role_data]}'

  return({'name':name,'price':price,'invoice':invoice_with_timestamp})