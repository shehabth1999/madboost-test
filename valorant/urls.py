from django.contrib import admin
from django.urls import path
from valorant.views import *

urlpatterns = [
  path('', valorantGetBoosterByRank, name='valorant'),
  path('paypal/', pay_with_paypal, name='valorant-paypal-redirect'),
  path('cryptomus/', pay_with_cryptomus, name='valorant-cryptomus-redirect'),
]
