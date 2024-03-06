from django.contrib import admin
from django.urls import path
from booster.views import *
from django.contrib.auth.decorators import user_passes_test

def is_booster(user):
    return user.is_authenticated and user.is_booster

urlpatterns = [
    path('register/',register_booster_view,name='booster.register'),
    path('edit_profile/', edit_booster_profile, name='edit.booster.profile'),
    path('profile/<booster_id>/',profile_booster_view,name='booster.profile'),
    path('rate/<int:order_id>/',get_rate,name='booster.rate'), # form to get rate if order done
    path('rating/<int:order_id>/', rate_page, name='rate.page'), # test page , only for test
    path('orders/', user_passes_test(is_booster)(booster_orders), name='booster.orders'),
    path('history/', user_passes_test(is_booster)(booster_history), name='booster.history'),
    path('can_choose_me/', CanChooseMe.as_view(), name='can_choose_me'),
    path('jobs/', jobs ,name='orders.jobs'),
    path('jobs/<str:game_name>/<int:id>/', calm_order, name='calm.order'),
    path('confirm_details/',confirm_details,name='confirm.details'),
    path('ask_customer/',ask_customer,name='ask.customer'),
    # path('get_latest_price/', get_latest_price, name='get_latest_price'),
    path('upload-image/',upload_finish_image,name='order.upload.image'),
    path('drop-order/',drop_order,name='drop.order'),
    path('update-rating/<int:order_id>',update_rating,name='order.update.rating'),
]
