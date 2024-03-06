from django.contrib import admin
from django.urls import path
from hearthstone.views import *

urlpatterns = [
  path('', hearthstoneGetBoosterByRank, name='hearthstone'),
  path('paypal/', view_that_asks_for_money, name='hearthstone-paypal-redirect'),
  path('payment-canceled/', payment_canceled ,name='hearthstone.payment.canceled'),
]