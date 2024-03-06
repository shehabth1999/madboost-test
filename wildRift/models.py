from django.shortcuts import render, redirect , HttpResponse, get_object_or_404
from django.db import models
from django.conf import settings
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from accounts.models import BaseOrder
from accounts.templatetags.custom_filters import romanize_division
import requests
import json

User = settings.AUTH_USER_MODEL

class WildRiftRank(models.Model):
    rank_name = models.CharField(max_length=25)
    rank_image = models.ImageField(upload_to='wildRift/images/', blank=True, null=True)

    def __str__(self):
        return self.rank_name
    
    def get_image_url(self):
        return f"/media/{self.rank_image}"

class WildRiftTier(models.Model):
    rank = models.OneToOneField('WildRiftRank', related_name='tier', on_delete=models.CASCADE)
    from_IV_to_III = models.FloatField(default=0)
    from_III_to_II = models.FloatField(default=0)
    from_II_to_I = models.FloatField(default=0)
    from_I_to_IV_next = models.FloatField(default=0)

    def __str__(self):
        return f"Tiers for {self.rank.rank_name}"

class WildRiftMark(models.Model):
    class MarkChoices(models.IntegerChoices):
        MARK_2 = 2, '2 Marks'
        MARK_3 = 3, '3 Marks'
        MARK_4 = 4, '4 Marks'
        MARK_5 = 5, '5 Marks'
        MARK_6 = 6, '6 Marks'

    rank = models.OneToOneField('WildRiftRank', related_name='mark', on_delete=models.CASCADE)
    tier = models.OneToOneField(WildRiftTier, related_name='tier_mark', on_delete=models.CASCADE)
    mark_number = models.IntegerField(choices=MarkChoices.choices)
    mark_1 = models.FloatField(default=0)
    mark_2 = models.FloatField(default=0)
    mark_3 = models.FloatField(default=0)
    mark_4 = models.FloatField(default=0)
    mark_5 = models.FloatField(default=0)
    mark_6 = models.FloatField(default=0)

    def __str__(self):
        return f"Mark {self.mark_number} for Tiers: {self.tier} in Rank: {self.rank.rank_name}"
    
class WildRiftDivisionOrder(models.Model):
    DIVISION_CHOICES = [
        (1, 'IV'),
        (2, 'III'),
        (3, 'II'),
        (4, 'I'),
    ]
    MARKS_CHOISES = [
        (0 , '0 Marks'),
        (1 , '1 Marks'),
        (2 , '2 Marks'),
        (3 , '3 Marks'),
        (4 , '4 Marks'),
        (5 , '5 Marks'),
        (6 , '6 Marks'),
    ]
    order = models.OneToOneField(BaseOrder, on_delete=models.CASCADE, primary_key=True, default=None, related_name='wildrift_order')
    current_rank = models.ForeignKey(WildRiftRank, on_delete=models.CASCADE, default=None, related_name='current_rank',blank=True, null=True)
    reached_rank = models.ForeignKey(WildRiftRank, on_delete=models.CASCADE, default=None, related_name='reached_rank',blank=True, null=True)
    desired_rank = models.ForeignKey(WildRiftRank, on_delete=models.CASCADE, default=None, related_name='desired_rank',blank=True, null=True)
    current_division = models.IntegerField(choices=DIVISION_CHOICES,blank=True, null=True)
    reached_division = models.IntegerField(choices=DIVISION_CHOICES,blank=True, null=True)
    desired_division = models.IntegerField(choices=DIVISION_CHOICES,blank=True, null=True)
    current_marks = models.IntegerField(choices=MARKS_CHOISES,blank=True, null=True)
    reached_marks = models.IntegerField(choices=MARKS_CHOISES,blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    booster_champions = models.BooleanField(default=False, blank=True)


    def send_discord_notification(self):
        if self.order.status == 'Extend':
            return print('Extend Order')
        discord_webhook_url = 'https://discord.com/api/webhooks/1190313898201583626/HtkVOsIBOEfj9Jl8eTO95ltrm36NVkKW-kq1a-XRPjOjC1UqXCMwy7t-s4DuOmxA5Ucs'
        current_time = self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        embed = {
            "title": "Rift",
            "description": (
                f"**Order ID:** {self.order.name}\n"
                f" From {str(self.current_rank).upper()} {romanize_division(self.current_division)} Marks {self.current_marks} "
                f" {str(self.current_rank).upper()} {romanize_division(self.current_division)} Marks {self.current_marks} To {str(self.desired_rank).upper()} {romanize_division(self.desired_division)} server us" # change server next
            ),
            "color": 0x3498db,  # Hex color code for a Discord blue color
            "footer": {"text": f"{current_time}"}, 
        }
        data = {
            "content": "New order has arrived \n",  # Set content to a space if you only want to send an embed
            "embeds": [embed],
        }


        headers = {
            "Content-Type": "application/json"
        }

        response = requests.post(discord_webhook_url, json=data, headers=headers)

        if response.status_code != 204:
            print(f"Failed to send Discord notification. Status code: {response.status_code}")

    def save_with_processing(self, *args, **kwargs):
        self.order.game_id = 1
        self.order.game_type = 'D'
        self.order.details = self.get_details()
        # 
        if not self.order.name:
            self.order.name = f'WR{self.order.id}'
        self.order.update_actual_price()
        self.order.save()
        super().save(*args, **kwargs)
        self.send_discord_notification()
    
    def get_details(self):
        return f"From {str(self.current_rank).upper()} {romanize_division(self.current_division)} Marks {self.current_marks} To {str(self.desired_rank).upper()} {romanize_division(self.desired_division)}"

    def __str__(self):
        return self.get_details()
    
    
    def get_rank_value(self, *args, **kwargs):
        return f"{self.current_rank.id},{self.current_division},{self.current_marks},{self.desired_rank.id},{self.desired_division},{self.order.duo_boosting},{self.order.select_booster},{self.order.turbo_boost},{self.order.streaming},{self.booster_champions}"
    

    def get_order_price(self):
        # Read data from JSON file
        with open('static/wildRift/data/divisions_data.json', 'r') as file:
            division_price = json.load(file)
            flattened_data = [item for sublist in division_price for item in sublist]
            flattened_data.insert(0,0)
        ##
        with open('static/wildRift/data/marks_data.json', 'r') as file:
            marks_data = json.load(file)
            marks_data.insert(0,[0,0,0,0,0,0,0])
        ##   
            
        promo_code_amount = self.order.promo_code
        if not promo_code_amount:
            promo_code_amount = 0

        current_rank = self.current_rank.id
        reached_rank = self.reached_rank.id

        current_division = self.current_division
        reached_division = self.reached_division

        current_marks = self.current_marks
        reached_marks = self.reached_marks

        total_percent = 0

        if self.order.duo_boosting:
            total_percent += 0.65

        if self.order.select_booster:
            total_percent += 0.10

        if self.order.turbo_boost:
            total_percent += 0.20

        if self.order.streaming:
            total_percent += 0.15

        if reached_rank != 8 :
            reached_division = 1

        start_division = ((current_rank-1)*4) + current_division
        end_division = ((reached_rank-1)*4)+ reached_division
        marks_price = marks_data[current_rank][current_marks]
        marks_price_reached = 0
        if reached_rank != 8:
            marks_price_reached = marks_data[reached_rank][reached_marks]

        sublist = flattened_data[start_division:end_division]


        total_sum = sum(sublist)    


        custom_price = total_sum - marks_price + marks_price_reached
        
        custom_price += (custom_price * total_percent)
        custom_price -= custom_price * (promo_code_amount/100)

        ##############################################################

        actual_price = self.order.actual_price
        main_price = self.order.price

        percent = round(actual_price / (main_price/100))

        print(percent)

        booster_price = custom_price * (percent/100)

        percent_for_view = round((booster_price/actual_price)* 100)
        if percent_for_view > 100:
            percent_for_view = 100

        if booster_price > actual_price:
            booster_price = actual_price


        return {"booster_price":booster_price, 'percent_for_view':percent_for_view}