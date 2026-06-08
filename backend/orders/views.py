from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from carts.models import Cart
from orders.models import Order, OrderItem
from orders.serializers import OrderSerializer
from orders.utils import send_order_notification


# <--- Place Order View --->
class PlaceOrderView(APIView):

    # Check if the User is Authenticated
    permission_classes = [IsAuthenticated]

    # Check if the Cart is empty
    def post(self, request):
        
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            return Response({"error": "No cart found for this user"})

        # shipping_address = request.data.get("shippingAddress")
        # if not cart or cart.cart_items.count() == 0:
        #     return Response({"error": "Cart is empty"})
        if not cart.cart_items.exists():
            return Response({"error": "Cart is empty"})

        # Create the Order
        order = Order.objects.create(
            user = request.user,
            subtotal = cart.subtotal,
            tax_amount = cart.tax_amount,
            grand_total = cart.grand_total,
            status = "CONFIRMED",
            # address = shipping_address.get("address"),
            # phone = shipping_address.get("phone"),
            # city = shipping_address.get("city"),
            # state = shipping_address.get("state"),
            # zip_code = shipping_address.get("zip_code")
        )

        # Create the Items Snapshot for the Order 
        for item in cart.cart_items.all():
            OrderItem.objects.create(
                order = order,
                product = item.product,
                quantity = item.quantity,
                price = item.product.product_price,
                total_price = item.total_price
            )

        # Clear the Cart after Processing the Order and Order Items Snapshot
        cart.cart_items.all().delete()
        cart.delete()
        cart.save()

        # Send Notification Email to User
        send_order_notification(order)


        # Send Response to the frontend
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

# <--- Order List View --->
class MyOrdersView(ListAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self): # pyright: ignore

        return Order.objects.filter(user=self.request.user)


# <--- Order Details View --->
class OrderDetailView(RetrieveAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer
    
    def get_object(self): # pyright: ignore

        pk = self.kwargs.get('order_id')
        order = get_object_or_404(Order, pk=pk, user=self.request.user)
        return order

