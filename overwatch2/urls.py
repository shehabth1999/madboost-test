from django.urls import path
from overwatch2.views import *

urlpatterns = [
  path('', overwatch2GetBoosterByRank, name='overwatch2'),
  path('paypal/', view_that_asks_for_money, name='overwatch2-paypal-redirect'),
  path('cryptomus/', view_that_asks_for_money, name='overwatch2-cryptomus-redirect'),
]