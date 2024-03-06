import json
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from accounts.models import BaseOrder
from accounts.controller.utils import live_orders

class OrderConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = 'orders'
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        all_orders_dict= live_orders()

        self.accept()
        self.send(text_data=json.dumps({
            'type':'order',
            'order':all_orders_dict,
        }))

    def order_list(self, event):
        order = event['order']
        self.send(text_data=json.dumps({
            'type':'order',
            'order': order,
        }))     

    # # # #    to receive message from js and auto send to others    

    # def receive(self, text_data):
    #     text_data_json = json.loads(text_data)
    #     order = text_data_json['order']
    #     user = text_data_json['user']
    #     order_with_user =[order,user]

    #     # self.send(text_data=json.dumps({
    #     #     'type':'order',
    #     #     'order':order,
    #     # }))

    #     async_to_sync(self.channel_layer.group_send)(
    #         self.room_group_name,
    #         {
    #             'type':'order_list',
    #             'order':'hi'
    #         }
    #     )

class PriceConsumer(WebsocketConsumer):
    def connect(self):
        self.order_id = self.scope['url_route']['kwargs']['order_id']
        self.group_name = f"price_updates_{self.order_id}"

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        self.accept()
        details = BaseOrder.objects.get(id=self.order_id).update_actual_price()
        self.send(text_data=json.dumps({
            'type':'time_with_price',
            'time':details['time'],
            'price':details['price'],
            
        }))

    # def disconnect(self):
    #     # Leave room group
    #     self.channel_layer.group_discard(
    #         self.group_name,
    #         self.channel_name,
    #     )

    def receive(self, text_data):
        details = BaseOrder.objects.get(id=self.order_id).update_actual_price()
        self.send(text_data=json.dumps({
            'type':'update_price',
            'time':details['time'],
            'price':details['price'],
        }))


    def update_price(self, event):
        price = event['price']
        time = event['time']
        print('all work good bro')
        self.send(text_data=json.dumps({
            'type':'update_price',
            'time':time,
            'price':price,
        }))
        
