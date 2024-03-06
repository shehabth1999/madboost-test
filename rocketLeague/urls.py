from django.contrib import admin
from django.urls import path
from rocketLeague.views import *

urlpatterns = [
  path('', rocketLeagueGetBoosterByRank, name='rocketLeague'),
  path('paypal/', pay_with_paypal, name='rocketLeague-paypal-redirect'),
  path('cryptomus/', pay_with_cryptomus, name='rocketLeague-cryptomus-redirect'),
]