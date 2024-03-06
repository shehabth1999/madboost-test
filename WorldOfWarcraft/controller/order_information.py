from django.shortcuts import get_object_or_404
import json
from django.utils import timezone
from WorldOfWarcraft.models import WoW_25_RPs_Price_2x2, BaseOrder
from django.contrib.auth import get_user_model
User = get_user_model()
rank_names = ['UNRANK', '0-1600', '1600-1800', '1800-2100', '2100-2500']


def get_arena_order_result_by_rank(data,extend_order_id):
  print('Data: ', data)
  # Division
  current_RP = data['current_RP']
  desired_RP = data['desired_RP']

  total_percent = 0
  duo_boosting = data['duo_boosting']
  select_booster = data['select_booster']
  turbo_boost = data['turbo_boost']
  streaming = data['streaming']
  choose_agents = data['choose_agents']

  duo_boosting_value = 0
  select_booster_value = 0
  turbo_boost_value = 0
  streaming_value = 0
  choose_agents_value = 0

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

  if choose_agents:
    total_percent += 0.0
    boost_options.append('CHOOSE AGENTS')
    choose_agents_value = 1
      
  wow_25_RPs_Price_2x2 = WoW_25_RPs_Price_2x2.objects.all().first().price
  total_sum = (desired_RP - current_RP) * (wow_25_RPs_Price_2x2 * 50)
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

  if current_RP >= 2100:
    current_rank = 4
  elif current_RP <= 2100 and current_RP >= 1800:
    current_rank = 3
  elif current_RP <= 1800 and current_RP >= 1600:
    current_rank = 2
  else:
    current_rank = 1
  
  if desired_RP >= 2100:
    desired_rank = 4
  elif desired_RP <= 2100 and desired_RP >= 1800:
    desired_rank = 3
  elif desired_RP <= 1800 and desired_RP >= 1600:
    desired_rank = 2
  else:
    desired_rank = 1
  
  
  invoice = f'WOW-6-A-{current_rank}-{current_RP}-0-{desired_rank}-{desired_RP}-{duo_boosting_value}-{select_booster_value}-{turbo_boost_value}-{streaming_value}-{booster_id}-{price}-{extend_order_id}-{timezone.now()}-?-{choose_agents_value}'
  print('Invoice', invoice)

  invoice_with_timestamp = str(invoice)
  boost_string = " WITH " + " AND ".join(boost_options) if boost_options else ""
  name = f'WOW, BOOSTING FROM {rank_names[current_rank]} {current_RP} TO {rank_names[desired_rank]} {desired_RP}{boost_string}'

  return({'name':name,'price':price,'invoice':invoice_with_timestamp})