from django.urls import path
from WorldOfWarcraft.views import *

urlpatterns = [
  path('', wowGetBoosterByRank, name='wow'),
  path('paypal/', view_that_asks_for_money, name='wow-paypal-redirect'),
  path('payment-canceled/', payment_canceled ,name='wow.payment.canceled'),
]