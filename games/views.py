from django.shortcuts import render
from games.models import Game

# Create your views here.
def games(request):
  games = Game.objects.all()

  context= {
    "games": games,
  }

  return render(request, 'games/games.html', context=context)