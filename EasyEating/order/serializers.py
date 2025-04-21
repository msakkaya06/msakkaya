from rest_framework import serializers
from easymanagement.models import Produce, Cart, CartItem, Order, OrderItem, ProduceType

# Produce modelinin serializer'ı
class ProduceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produce
        fields = ['id', 'name', 'price', 'image', 'produceType']

# CartItem modelinin serializer'ı
class CartItemSerializer(serializers.ModelSerializer):
    produce = ProduceSerializer()

    class Meta:
        model = CartItem
        fields = ['id', 'produce', 'quantity', 'unit_price']

# Cart modelinin serializer'ı
class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(source='cartitem_set', many=True)

    class Meta:
        model = Cart
        fields = ['id', 'cart_items', 'isActive']

# OrderItem modelinin serializer'ı
class OrderItemSerializer(serializers.ModelSerializer):
    produce = ProduceSerializer()

    class Meta:
        model = OrderItem
        fields = ['id', 'produce', 'quantity', 'unit_price']

# Order modelinin serializer'ı
class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(source='orderitem_set', many=True)

    class Meta:
        model = Order
        fields = ['id', 'status', 'total_price', 'order_items']
