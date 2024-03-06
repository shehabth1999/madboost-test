from django.shortcuts import render, redirect,get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.http import JsonResponse
from django.http import HttpResponse
from django.urls import reverse, reverse_lazy
import json
from django.conf import settings
from mobileLegends.models import *
from mobileLegends.controller.serializers import DivisionSerializer, PlacementSerializer
from django.contrib.auth import get_user_model
from django.utils import timezone
from paypal.standard.forms import PayPalPaymentsForm
from mobileLegends.controller.order_information import *

# Create your views here.
@csrf_exempt
def MobileLegendsGetBoosterByRank(request):
  extend_order = request.GET.get('extend')
  try:
    order_get_rank_value = MobileLegendsDivisionOrder.objects.get(order_id=extend_order).get_rank_value()
  except:
    order_get_rank_value = None
  ranks = MobileLegendsRank.objects.all().order_by('id')
  divisions  = MobileLegendsTier.objects.all().order_by('id')
  marks = MobileLegendsMark.objects.all().order_by('id')
  placements = MobileLegendsPlacement.objects.all().order_by('id')

  divisions_data = [
    [division.from_V_to_IV ,division.from_IV_to_III, division.from_III_to_II, division.from_II_to_I, division.from_I_to_V_next]
    for division in divisions
  ]
  

  marks_data = [
    [mark.star_1, mark.star_2, mark.star_3, mark.star_4, mark.star_5]
    for mark in marks
  ]
  placements_data = [
    placement.price
    for placement in placements
  ]

  with open('static/mobileLegends/data/divisions_data.json', 'w') as json_file:
    json.dump(divisions_data, json_file)

  with open('static/mobileLegends/data/marks_data.json', 'w') as json_file:
    json.dump(marks_data, json_file)

  with open('static/mobileLegends/data/placements_data.json', 'w') as json_file:
    json.dump(placements_data, json_file)

  divisions_list = list(divisions.values())
  context = {
    "ranks": ranks,
    "divisions": divisions_list,
    "placements": placements,
    "order_get_rank_value":order_get_rank_value,
  }
  return render(request,'mobileLegends/GetBoosterByRank.html', context)

# Paypal
@csrf_exempt
def view_that_asks_for_money(request):
  print('hi')
  if request.method == 'POST':
    if request.user.is_authenticated :
      if request.user.is_booster:
        messages.error(request, "You are a booster!, You can't make order.")
        return redirect(reverse_lazy('mobileLegends'))
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
          print('Order Info: ', order_info)
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