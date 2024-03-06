from django.urls import path
from games.views import *

urlpatterns = [
  path('', games, name="games.games"),
]