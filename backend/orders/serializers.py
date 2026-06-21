from rest_framework import serializers
from orders.models import Order, OrderItem


# <--- Order Item Serializer --->
class OrderItemSerialzier(serializers.ModelSerializer):

    product_name = serializers.CharField(source="product.product_name", read_only=True)

    class Meta:
        model = OrderItem
        fields = "__all__"


# <--- Order Serializer --->
class OrderSerializer(serializers.ModelSerializer):

    items = OrderItemSerialzier(source="orderitem_set", many=True, read_only=True)

    class Meta:
        model = Order
        fields = "__all__"
