from django.shortcuts import render
from booster.models import OrderRating
from games.models import Game
from accounts.models import BaseOrder

import json

def index(request):

  games = Game.objects.all()

  base_orders_query = list(BaseOrder.objects.filter(is_done=True))

  divsion_orders = []

  placement_orders = []

  for order in base_orders_query:
    content_type = order.content_type
    if content_type:
      last_order = content_type.model_class().objects.get(order_id=order.object_id)

      if last_order.order.game_type == 'D':
        divsion_orders.append(last_order)

      elif last_order.order.game_type == 'P':
        placement_orders.append(last_order)


  last_orders = list(divsion_orders) + list(placement_orders)

  feedbacks = OrderRating.objects.all()

  context= {
    "games": games,
    "feedbacks": feedbacks,
    "last_orders": last_orders,
  }

  return render(request, 'homepage/index.html', context=context)
