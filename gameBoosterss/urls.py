from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from gameBoosterss.views import index

urlpatterns = [
    path('', index, name="homepage.index"),
    path('admin/', admin.site.urls),
    path('customer/', include('customer.urls')),
    path('booster/', include('booster.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('wildRift/', include('wildRift.urls')),
    path('accounts/', include('accounts.urls')),
    path('valorant/', include('valorant.urls')),
    path('lol/', include('leagueOfLegends.urls')),
    path('pubg/', include('pubg.urls')),
    path('wow/', include('WorldOfWarcraft.urls')),
    path('tft/', include('tft.urls')),
    path('hearthstone/', include('hearthstone.urls')),
    path('rocketLeague/', include('rocketLeague.urls')),
    path('mobileLegends/', include('mobileLegends.urls')),
    path('dota2/', include('dota2.urls')),
    path('overwatch2/', include('overwatch2.urls')),
    path('csgo2/', include('csgo2.urls')),
    path('hok/', include('honorOfKings.urls')),
    path('games/', include('games.urls')),
    path('paypal/', include("paypal.standard.ipn.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)