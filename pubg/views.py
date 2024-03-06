from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.http import JsonResponse
from django.http import HttpResponse
from django.urls import reverse, reverse_lazy
import json
from django.conf import settings
from pubg.models import *
from pubg.controller.serializers import DivisionSerializer
from paypal.standard.forms import PayPalPaymentsForm
from pubg.controller.order_information import *

@csrf_exempt
def pubgGetBoosterByRank(request):
  extend_order = request.GET.get('extend')
  try:
    order = PubgDivisionOrder.objects.get(order_id=extend_order)
  except:
    order = None
  ranks = PubgRank.objects.all().order_by('id')
  divisions  = PubgTier.objects.all().order_by('id')
  marks = PubgMark.objects.all().order_by('id')

  divisions_data = [
    [division.from_V_to_VI, division.from_VI_to_III, division.from_III_to_II, division.from_II_to_I]
    for division in divisions
  ]
  
  marks_data = [
    [mark.marks_0_20, mark.marks_21_40, mark.marks_41_60, mark.marks_61_80, mark.marks_81_100]
    for mark in marks
  ]

  with open('static/pubg/data/divisions_data.json', 'w') as json_file:
    json.dump(divisions_data, json_file)
    
  with open('static/pubg/data/marks_data.json', 'w') as json_file:
    json.dump(marks_data, json_file)

  divisions_list = list(divisions.values())
  context = {
    "ranks": ranks,
    "divisions": divisions_list,
    "order":order,
  }
  return render(request,'pubg/GetBoosterByRank.html', context)


# Paypal
@csrf_exempt
def view_that_asks_for_money(request):
  if request.method == 'POST':
    if request.user.is_authenticated :
      if request.user.is_booster:
        messages.error(request, "You are a booster!, You can't make order.")
        return redirect(reverse_lazy('pubg'))
      
    print('request POST:  ', request.POST)
    try:
      # Division
      serializer = DivisionSerializer(data=request.POST)

      if serializer.is_valid():
        extend_order_id = serializer.validated_data['extend_order']
        # Division
        order_info = get_division_order_result_by_rank(serializer.validated_data,extend_order_id)

        request.session['invoice'] = order_info['invoice']

        paypal_dict = {
            "business": settings.PAYPAL_EMAIL,
            "amount": order_info['price'],
            "item_name": order_info['name'],
            "invoice": order_info['invoice'],
            "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
            "return": request.build_absolute_uri(f"/accounts/register/"),
            "cancel_return": request.build_absolute_uri(f"/pubg/payment-canceled/"),
        }
        # Create the instance.
        form = PayPalPaymentsForm(initial=paypal_dict)
        context = {"form": form}
        return render(request, "pubg/paypal.html", context,status=200)
      return JsonResponse({'error': serializer.errors}, status=400)
      # messages.error(request, 'Ensure this value is greater than or equal to 10')
      # return redirect(reverse_lazy('pubg'))
    except Exception as e:
      return JsonResponse({'error': f'Error processing form data: {str(e)}'}, status=400)

  return JsonResponse({'error': 'Invalid request method. Use POST.'}, status=400)

# Cancel Payment
def payment_canceled(request):
  return HttpResponse('payment canceled')