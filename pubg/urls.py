from django.urls import path
from .views import *

urlpatterns = [
  path('', pubgGetBoosterByRank, name='pubg'),
  path('paypal/', view_that_asks_for_money, name='pubg-paypal-redirect'),
  path('payment-canceled/', payment_canceled ,name='pubg.payment.canceled'),
]