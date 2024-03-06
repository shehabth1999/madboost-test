from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.http import JsonResponse
from django.http import HttpResponse
from django.urls import reverse, reverse_lazy
import json
from django.conf import settings
from honorOfKings.models import *
from honorOfKings.controller.serializers import DivisionSerializer
from paypal.standard.forms import PayPalPaymentsForm
from honorOfKings.controller.order_information import *
from booster.models import OrderRating

# Create your views here.
@csrf_exempt
def honerOfKingeGetBoosterByRank(request):
  extend_order = request.GET.get('extend')
  try:
    order = HonorOfKingsDivisionOrder.objects.get(order_id=extend_order)
  except:
    order = None
  ranks = HonorOfKingsRank.objects.all().order_by('id')
  divisions  = HonorOfKingsTier.objects.all().order_by('id')
  marks = HonorOfKingsMark.objects.all().order_by('id')

  divisions_data = [
    [division.from_V_to_IV, division.from_IV_to_III, division.from_III_to_II, division.from_II_to_I, division.from_I_to_IV_next]
    for division in divisions
  ]

  marks_data = [
    [0, mark.star_1, mark.star_2, mark.star_3]
    for mark in marks
  ]

  with open('static/hok/data/divisions_data.json', 'w') as json_file:
    json.dump(divisions_data, json_file)

  with open('static/hok/data/marks_data.json', 'w') as json_file:
    json.dump(marks_data, json_file)

  divisions_list = list(divisions.values())

  # Feedbacks
  feedbacks = OrderRating.objects.filter(order__game_id = 11)
  context = {
    "ranks": ranks,
    "divisions": divisions_list,
    "order":order,
    "feedbacks": feedbacks,
  }
  return render(request,'honorOfKings/GetBoosterByRank.html', context)

# Paypal
@csrf_exempt
def view_that_asks_for_money(request):
  if request.method == 'POST':
    if request.user.is_authenticated :
      if request.user.is_booster:
        messages.error(request, "You are a booster!, You can't make order.")
        return redirect(reverse_lazy('hok'))
      
    print('request POST:  ', request.POST)
    try:
      serializer = DivisionSerializer(data=request.POST)

      if serializer.is_valid():
        extend_order_id = serializer.validated_data['extend_order']
      
        order_info = get_division_order_result_by_rank(serializer.validated_data,extend_order_id)
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
      # return JsonResponse({'error': serializer.errors}, status=400)
      messages.error(request, 'Ensure this value is greater than or equal to 10')
      return redirect(reverse_lazy('hok'))
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