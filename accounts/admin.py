from django.contrib import admin

# Register your models here.

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import BaseUser, BaseOrder, Room, Message, Wallet, Transaction, BoosterPercent, TokenForPay, Tip_data, PromoCode

class CustomUserAdmin(UserAdmin):
    # Customize the display fields for the user model
    list_display = ('username', 'email', 'is_staff','is_active','is_booster','is_customer','is_admin')
    search_fields = ('email', 'username',)
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'profile_image')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'country')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser','is_booster','is_customer','is_admin')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

admin.site.register(BaseUser ,CustomUserAdmin)
admin.site.register(BaseOrder)
admin.site.register(Room)
admin.site.register(Message)
admin.site.register(Wallet)
admin.site.register(Transaction)
admin.site.register(BoosterPercent)
admin.site.register(TokenForPay)
admin.site.register(Tip_data)
admin.site.register(PromoCode)