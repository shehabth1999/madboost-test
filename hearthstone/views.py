from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.http import JsonResponse
from django.http import HttpResponse
from django.urls import reverse, reverse_lazy
import json
from django.conf import settings
from hearthstone.models import *
from hearthstone.controller.serializers import DivisionSerializer
from paypal.standard.forms import PayPalPaymentsForm
from hearthstone.controller.order_information import *

# Create your views here.
@csrf_exempt
def hearthstoneGetBoosterByRank(request):
  extend_order = request.GET.get('extend')
  try:
    order = HearthstoneDivisionOrder.objects.get(order_id=extend_order)
  except:
    order = None
  ranks = HearthstoneRank.objects.all().order_by('id')
  divisions  = HearthstoneTier.objects.all().order_by('id')
  marks = HearthstoneMark.objects.all().order_by('id')

  divisions_data = [
    [division.from_X_to_IX, division.from_IX_to_VIII, division.from_VIII_to_VII, division.from_VII_to_VI, division.from_VI_to_V, division.from_V_to_IV, division.from_IV_to_III, division.from_III_to_II, division.from_II_to_I, division.from_I_to_IV_next]
    for division in divisions
  ]

  marks_data = [
    [mark.marks_3, mark.marks_2, mark.marks_1]
    for mark in marks
  ]

  with open('static/hearthstone/data/divisions_data.json', 'w') as json_file:
    json.dump(divisions_data, json_file)

  with open('static/hearthstone/data/marks_data.json', 'w') as json_file:
    json.dump(marks_data, json_file)

  divisions_list = list(divisions.values())
  context = {
    "ranks": ranks,
    "divisions": divisions_list,
    "order":order,
  }
  return render(request,'hearthstone/GetBoosterByRank.html', context)

# Paypal
@csrf_exempt
def view_that_asks_for_money(request):
  if request.method == 'POST':
    if request.user.is_authenticated :
      if request.user.is_booster:
        messages.error(request, "You are a booster!, You can't make order.")
        return redirect(reverse_lazy('hearthstone'))
      
    print('request POST:  ', request.POST)
    try:
      # Division
      if request.POST.get('game_type') == 'D':
        serializer = DivisionSerializer(data=request.POST)

      if serializer.is_valid():
        extend_order_id = serializer.validated_data['extend_order']
        # Division
        if request.POST.get('game_type') == 'D':
          order_info = get_division_order_result_by_rank(serializer.validated_data,extend_order_id)
          print('Order Info: ', order_info)

        request.session['invoice'] = order_info['invoice']

        paypal_dict = {
          "business": settings.PAYPAL_EMAIL,
          "amount": order_info['price'],
          "item_name": order_info['name'],
          "invoice": order_info['invoice'],
          "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
          "return": request.build_absolute_uri(f"/accounts/register/"),
          "cancel_return": request.build_absolute_uri(f"/hearthstone/payment-canceled/"),
        }
        # Create the instance.
        form = PayPalPaymentsForm(initial=paypal_dict)
        context = {"form": form}
        return render(request, "hearthstone/paypal.html", context,status=200)
      # return JsonResponse({'error': serializer.errors}, status=400)
      messages.error(request, 'Ensure this value is greater than or equal to 10')
      return redirect(reverse_lazy('hearthstone'))
    except Exception as e:
      return JsonResponse({'error': f'Error processing form data: {str(e)}'}, status=400)

  return JsonResponse({'error': 'Invalid request method. Use POST.'}, status=400)

# Cancel Payment
def payment_canceled(request):
  return HttpResponse('payment canceled')