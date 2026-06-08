from rest_framework import serializers
from orders.models import Order, OrderItem


# <--- Order Serializer --->
class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = "__all__"


# <--- Order Item Serializer --->
class OrderItemSerialzier(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = "__all__"    
