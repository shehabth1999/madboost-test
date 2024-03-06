from django.contrib import admin
from django.urls import path
from honorOfKings.views import *

urlpatterns = [
  path('', honerOfKingeGetBoosterByRank, name='hok'),
  path('paypal/', view_that_asks_for_money, name='hok-paypal-redirect'),
  path('cryptomus/', pay_with_cryptomus, name='hok-cryptomus-redirect'),
]