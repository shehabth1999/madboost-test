from django.contrib import admin
from django.urls import path, include
from accounts.views import *
from django.contrib.auth.decorators import user_passes_test

def is_customer(user):
    return user.is_authenticated and (user.is_customer or not user.is_booster)

urlpatterns = [
    path('register/', register_view, name='accounts.register'),
    path('profile/', profile_view, name='accounts.profile'),
    path('activate/<str:uidb64>/<str:token>/', activate_account, name='account.activate'),
    path('login/', login_view, name='account.login'),
    path('logout/', logout_view, name='account.logout'), 
    path('choose_booster/', choose_booster, name='choose.booster'),
    path('set_customer_data/', set_customer_data, name='set.customer.data'),
    path('tip_booster/', tip_booster, name='tip_booster'),
    path('tip_booster/success/<str:token>/', success_tip, name='tip_booster.success_tip'),
    path('tip_booster/cancel/<str:token>/', cancel_tip, name='tip_booster.cancel_tip'),
    path('customer_side/', user_passes_test(is_customer)(customer_side), name='accounts.customer_side'),
    path('edit_profile/', user_passes_test(is_customer)(edit_customer_profile), name='edit.customer.profile'),
    path('history/', user_passes_test(is_customer)(customer_history), name='customer.history'),
    path('test/', test, name='test'),
    path('payment-canceled/', payment_canceled ,name='payment.canceled'),
    # path('create_job/<int:id>/',create_background_job_to_change_order_price,name='create_job')
    # path('order-list/', order_list, name='order.list'),
    # path('create_order/', submit_order, name='order.create'),
    path('promo-codes/', PromoCodeAPIView.as_view(), name='promo_code_detail'),
    
]