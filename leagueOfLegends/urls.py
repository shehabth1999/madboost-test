from django.contrib import admin
from django.urls import path
from leagueOfLegends.views import *

urlpatterns = [
  path('', leagueOfLegendsGetBoosterByRank, name='lol'),
  path('paypal/', view_that_asks_for_money, name='lol-paypal-redirect'),
  path('payment-canceled/', payment_canceled ,name='lol.payment.canceled'),
]