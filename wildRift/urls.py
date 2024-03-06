from django.contrib import admin
from django.urls import path
from wildRift.views import *

urlpatterns = [
    path('', wildRiftGetBoosterByRank, name='wildRift'),
    path('paypal/', pay_with_paypal, name='wildRift-paypal-redirect'),
    path('cryptomus/', pay_with_cryptomus, name='wildRift-cryptomus-redirect'),
    # path('test/<int:order_id>/',get_update_order_result, name='testooo')
]
