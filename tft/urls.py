from django.contrib import admin
from django.urls import path
from tft.views import *

urlpatterns = [
  path('', tftGetBoosterByRank, name='tft'),
  path('paypal/', view_that_asks_for_money, name='tft-paypal-redirect'),
  path('payment-canceled/', payment_canceled ,name='tft.payment.canceled'),
]