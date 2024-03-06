from django.shortcuts import render, redirect,get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse, reverse_lazy
import json
from django.conf import settings
from rocketLeague.models import *
from rocketLeague.controller.serializers import *
from paypal.standard.forms import PayPalPaymentsForm
from rocketLeague.controller.order_information import *
from booster.models import OrderRating

# Create your views here.

@csrf_exempt
def rocketLeagueGetBoosterByRank(request):
  extend_order = request.GET.get('extend')
  try:
    order = RocketLeagueDivisionOrder.objects.get(order_id=extend_order)
  except:
    order = None
  ranks = RocketLeagueRank.objects.all().order_by('id')
  divisions  = RocketLeagueDivision.objects.all().order_by('id')
  placements = RocketLeaguePlacement.objects.all().order_by('id')
  seasonals = RocketLeagueSeasonal.objects.all().order_by('id')
  tournaments = RocketLeagueTournament.objects.all().order_by('id')

  divisions_data = [
    [division.from_I_to_II, division.from_II_to_III, division.from_III_to_I_next]
    for division in divisions
  ]

  placements_data = [
    placement.price
    for placement in placements
  ]

  seasonals_data = [
    seasonal.price
    for seasonal in seasonals
  ]

  tournaments_data = [
    seasonal.price
    for seasonal in tournaments
  ]

  with open('static/rocketLeague/data/divisions_data.json', 'w') as json_file:
    json.dump(divisions_data, json_file)

  with open('static/rocketLeague/data/placements_data.json', 'w') as json_file:
    json.dump(placements_data, json_file)

  with open('static/rocketLeague/data/seasonals_data.json', 'w') as json_file:
    json.dump(seasonals_data, json_file)

  with open('static/rocketLeague/data/tournaments_data.json', 'w') as json_file:
    json.dump(tournaments_data, json_file)

  divisions_list = list(divisions.values())

  # Feedbacks
  feedbacks = OrderRating.objects.filter(order__game_name = "rocketLeague")
  context = {
    "ranks": ranks,
    "divisions": divisions_list,
    "placements": placements,
    "seasonals": seasonals,
    "tournaments": tournaments,
    "order":order,
    "feedbacks": feedbacks,
  }
  return render(request,'rocketLeague/GetBoosterByRank.html', context)

# Paypal
@csrf_exempt
def pay_with_paypal(request):
  if request.method == 'POST':
    if request.user.is_authenticated :
      if request.user.is_booster:
        messages.error(request, "You are a booster!, You can't make order.")
        return redirect(reverse_lazy('rocketLeague'))
      
    print('request POST:  ', request.POST)
    try:
      # Division
      if request.POST.get('game_type') == 'D':
        serializer = DivisionSerializer(data=request.POST)
      # Placement
      elif request.POST.get('game_type') == 'P':
        serializer = PlacementSerializer(data=request.POST)
      # Seasonal
      elif request.POST.get('game_type') == 'S':
        serializer = SeasonalSerializer(data=request.POST)
      # Tournament
      elif request.POST.get('game_type') == 'T':
        serializer = TournamentSerializer(data=request.POST)

      if serializer.is_valid():
        extend_order_id = serializer.validated_data['extend_order']
        # Division
        if request.POST.get('game_type') == 'D':
          order_info = get_division_order_result_by_rank(serializer.validated_data,extend_order_id)
        # Placement
        elif request.POST.get('game_type') == 'P':
          order_info = get_palcement_order_result_by_rank(serializer.validated_data,extend_order_id)
        # Seasonal
        elif request.POST.get('game_type') == 'S':
          order_info = get_seasonal_order_result_by_rank(serializer.validated_data,extend_order_id)
        # Tournament
        elif request.POST.get('game_type') == 'T':
          order_info = get_tournament_order_result_by_rank(serializer.validated_data,extend_order_id)

        request.session['invoice'] = order_info['invoice']

        paypal_dict = {
            "business": settings.PAYPAL_EMAIL,
            "amount": order_info['price'],
            "item_name": order_info['name'],
            "invoice": order_info['invoice'],
            "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
            "return": request.build_absolute_uri(f"/accounts/register/"),
            "cancel_return": request.build_absolute_uri(f"/accounts/payment-canceled/"),
        }
        # Create the instance.
        form = PayPalPaymentsForm(initial=paypal_dict)
        context = {"form": form}
        return render(request, "accounts/paypal.html", context,status=200)
      return JsonResponse({'error': serializer.errors}, status=400)
      # messages.error(request, 'Ensure this value is greater than or equal to 10')
      # return redirect(reverse_lazy('rocketLeague'))
    except Exception as e:
      return JsonResponse({'error': f'Error processing form data: {str(e)}'}, status=400)

  return JsonResponse({'error': 'Invalid request method. Use POST.'}, status=400)

# Cryptomus
@csrf_exempt
def pay_with_cryptomus(request):
  if request.method == 'POST':
    context = {
      "data": request.POST
    }
    return render(request, "accounts/cryptomus.html", context,status=200)
  return render(request, "accounts/cryptomus.html", context={"data": "There is error"},status=200)