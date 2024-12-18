# myapp/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from decimal import Decimal

from easymanagement.models import Cart,Order, Desk


class BusinessConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.business_id = self.scope['url_route']['kwargs']['business_id']
        self.room_group_name = f'business_{self.business_id}'

        # Join the business group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the business group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        order_id = text_data_json['order_id']

        # Fetch the updated order data
        order = Order.objects.get(id=order_id)
        order_data = {
            'order_id': order.id,
            'status': order.status,
            'total_price': order.total_price,
            'created_at': order.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'items': list(order.orderitem_set.values('id', 'produce__name', 'quantity', 'unit_price')),
            'desk_id': order.desk.id,
            'desk_name': order.desk.name,
        }
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send_order_update',
                'order_data': order_data,  # Order data gönderiliyor
            }
        )


    async def send_order_update(self, event):
        order_data = event['order_data']
        total_price = order_data['total_price'] if order_data['total_price'] is not None else 0.0

        # 'items' içindeki 'unit_price' değerlerini float'a çeviriyoruz
        items = order_data['items']
        for item in items:
            item['unit_price'] = float(item['unit_price'])  # Her bir ürünün fiyatını float'a çeviriyoruz

        # JSON formatında gönder
        await self.send(text_data=json.dumps({
            'type': 'order_update',
            'desk_id': order_data['desk_id'],
            'order_id': order_data['order_id'],
            'status': order_data['status'],
            'items': items,  # Güncellenmiş items listesi
            'desk_name': order_data['desk_name'],
        }))
    
    def decimal_default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        raise TypeError

           # Masa güncellemesini WebSocket üzerinden işleme
    async def send_desk_update(self, event):
        desk_data = event['desk_data']

        # Masa bilgilerini WebSocket üzerinden frontend'e gönder
        await self.send(text_data=json.dumps({
            'desk_data': desk_data
        }))

class DeskConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.desk_slug = self.scope['url_route']['kwargs']['desk_slug']
        self.room_group_name = f'desk_{self.desk_slug}'

        # Join the desk group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the desk group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        cart_id = text_data_json['cart_id']

        # Fetch the updated cart data
        cart = Cart.objects.get(id=cart_id)
        cart_items = list(cart.cartitem_set.values('produce__name', 'quantity', 'unit_price'))
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'cart_update',
                'cart_items': cart_items,
                'total_price': cart.calculate_total_price(),
            }
        )

    async def cart_update(self, event):
        await self.send(text_data=json.dumps(event))
