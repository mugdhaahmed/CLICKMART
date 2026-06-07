from rest_framework import serializers
from .models import Cart, CartItem


# <--- Nested Serializer for Cart Items --->
class CartItemSerializer(serializers.ModelSerializer):

    product_name = serializers.CharField(source="product.product_name")
    product_price = serializers.DecimalField(source="product.product_price", max_digits=6, decimal_places=2)
    product_tax_percentage = serializers.DecimalField(source="product.product_tax_percentage", max_digits=3, decimal_places=2)

    class Meta:
        model = CartItem
        fields = "__all__"


# <--- Cart Serialzier --->
class CartSerializer(serializers.ModelSerializer):

    cart_items = CartItemSerializer(many=True, read_only=True, source="cart_items")
    subtotal = serializers.DecimalField(max_digits=6, decimal_places=2)
    grand_total = serializers.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        model = Cart
        fields = "__all__"