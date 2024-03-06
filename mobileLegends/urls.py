from django.urls import path
from mobileLegends.views import *

urlpatterns = [
  path('', MobileLegendsGetBoosterByRank, name='mobileLegends'),
  path('paypal/', view_that_asks_for_money, name='mobileLegends-paypal-redirect'),
  path('paypal/', view_that_asks_for_money, name='mobileLegends-cryptomus-redirect'),
]
