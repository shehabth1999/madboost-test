from django.urls import re_path
from .consumers import OrderConsumer, PriceConsumer

websocket_urlpatterns = [
    re_path(r'ws/order/',OrderConsumer.as_asgi()),
    re_path(r'ws/price/(?P<order_id>\d+)/$', PriceConsumer.as_asgi()),

] 