from django.shortcuts import render, redirect,get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.http import JsonResponse
from django.http import HttpResponse
from django.urls import reverse, reverse_lazy
import json
from django.conf import settings
from overwatch2.models import Overwatch2DivisionOrder, Overwatch2Rank, Overwatch2Mark, Overwatch2Tier, Overwatch2Placement
from overwatch2.controller.serializers import DivisionSerializer, PlacementSerializer
from django.contrib.auth import get_user_model
from django.utils import timezone
from paypal.standard.forms import PayPalPaymentsForm
from overwatch2.controller.order_information import *

# Create your views here.
@csrf_exempt
def overwatch2GetBoosterByRank(request):
  order_get_rank_value = None
  extend_order = request.GET.get('extend')
  if extend_order:
    try:
      order_get_rank_value = Overwatch2DivisionOrder.objects.get(order_id=extend_order, customer=request.user).get_rank_value()
    except:
      return redirect('homepage.index')
  ranks = Overwatch2Rank.objects.all().order_by('id')
  divisions  = Overwatch2Tier.objects.all().order_by('id')
  marks = Overwatch2Mark.objects.all().order_by('id')
  placements = Overwatch2Placement.objects.all().order_by('id')

  divisions_data = [
    [division.from_V_to_IV ,division.from_IV_to_III, division.from_III_to_II, division.from_II_to_I, division.from_I_to_V_next]
    for division in divisions
  ]
  

  marks_data = [
    [mark.mark_1, mark.mark_2, mark.mark_3, mark.mark_4, mark.mark_5]
    for mark in marks
  ]
  placements_data = [
    placement.price
    for placement in placements
  ]

  with open('static/overwatch2/data/divisions_data.json', 'w') as json_file:
    json.dump(divisions_data, json_file)

  with open('static/overwatch2/data/marks_data.json', 'w') as json_file:
    json.dump(marks_data, json_file)

  with open('static/overwatch2/data/placements_data.json', 'w') as json_file:
    json.dump(placements_data, json_file)

  divisions_list = list(divisions.values())
  context = {
    "ranks": ranks,
    "divisions": divisions_list,
    "placements": placements,
    "order_get_rank_value":order_get_rank_value,
  }
  return render(request,'overwatch2/GetBoosterByRank.html', context)

# Paypal
@csrf_exempt
def view_that_asks_for_money(request):
  if request.method == 'POST':
    if request.user.is_authenticated :
      if request.user.is_booster:
        messages.error(request, "You are a booster!, You can't make order.")
        return redirect(reverse_lazy('overwatch2'))
    try:
      # Division
      if request.POST.get('game_type') == 'D':
        serializer = DivisionSerializer(data=request.POST)
      # Placement
      elif request.POST.get('game_type') == 'P':
        serializer = PlacementSerializer(data=request.POST)

      if serializer.is_valid():
        extend_order_id = serializer.validated_data['extend_order']
        # Division
        if request.POST.get('game_type') == 'D':
          order_info = get_division_order_result_by_rank(serializer.validated_data,extend_order_id)
        # Placement
        elif request.POST.get('game_type') == 'P':
          order_info = get_palcement_order_result_by_rank(serializer.validated_data,extend_order_id)

        request.session['invoice'] = order_info['invoice']

        paypal_dict = {
            "business": settings.PAYPAL_EMAIL,
            "amount": order_info['price'],
            "item_name": order_info['name'],
            "invoice": order_info['invoice'],
            "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
            "return": request.build_absolute_uri(f"/accounts/register/"),
            "cancel_return": request.build_absolute_uri(f"/mobileLegends/payment-canceled/"),
        }
        # Create the instance.
        form = PayPalPaymentsForm(initial=paypal_dict)
        context = {"form": form}
        return render(request, "mobileLegends/paypal.html", context,status=200)
      # return JsonResponse({'error': serializer.errors}, status=400)
      messages.error(request, 'Ensure this value is greater than or equal to 10')
      return redirect(reverse_lazy('lol'))
    except Exception as e:
      return JsonResponse({'error': f'Error processing form data: {str(e)}'}, status=400)

  return JsonResponse({'error': 'Invalid request method. Use POST.'}, status=400)

# Cancel Payment
def payment_canceled(request):
  return HttpResponse('payment canceled')