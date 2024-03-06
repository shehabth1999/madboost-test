from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.http import JsonResponse
from django.http import HttpResponse
from django.urls import reverse, reverse_lazy
from django.conf import settings
from .models import *
from .controller.serializers import RankBoostSerializer
from paypal.standard.forms import PayPalPaymentsForm
from .controller.order_information import get_rank_boost_order_result_by_rank

def dota2GetBoosterByRank(request):
  extend_order = request.GET.get('extend')
  order_get_rank_value = None
  if extend_order:
    try:
      order_get_rank_value = Dota2RankBoostOrder.objects.get(order_id=extend_order).get_rank_value()
    except Dota2RankBoostOrder.DoesNotExist:
      return redirect('homepage.index')
  ranks = Dota2Rank.objects.all().order_by('id')    

  context = {
    "ranks": ranks,
    "order":order_get_rank_value,
  }
  return render(request,'dota2/GetBoosterByRank.html', context)


# Paypal
def view_that_asks_for_money(request):
  if request.method == 'POST':
    if request.user.is_authenticated :
      if request.user.is_booster:
        messages.error(request, "You are a booster!, You can't make order.")
        return redirect(reverse_lazy('dota2'))
    try:
      # Division
      serializer = RankBoostSerializer(data=request.POST)

      if serializer.is_valid():
        extend_order_id = serializer.validated_data['extend_order']
        # Arena
        order_info = get_rank_boost_order_result_by_rank(serializer.validated_data,extend_order_id)

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
        return render(request, "dota2/paypal.html", context,status=200)
      return JsonResponse({'error': serializer.errors}, status=400)
    except Exception as e:
      return JsonResponse({'error': f'Error processing form data: {str(e)}'}, status=400)

  return JsonResponse({'error': 'Invalid request method. Use POST.'}, status=400)

