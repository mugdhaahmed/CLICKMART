from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from products.models import Product
from rest_framework import status


# <--- Cart List View --->
# Get or Create Cart of the User Directly from the Cart Page ('.../cart/')
class CartListView(APIView):
    
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)
    

# <--- Add to Cart View --->
# Get or Create the Cart of the User Directly from the Product Page ('.../product/...')
class AddToCartView(APIView):

    permission_classes = [IsAuthenticated]

    # Add Product to the Cart
    def post(self, request):

        # Take product_id and quantity from the frontend to add into the cart
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity')

        # if product_id is not provided, return error, else Fetch the product details from the product model
        if not product_id: 
            return Response({"error":"product_id is required!"})
        else: 
            product = get_object_or_404(Product, id=product_id, product_is_active=True)

        # Fetch the Cart of the associated user
        cart, _ = Cart.objects.get_or_create(user=request.user)

        # if cart is created and item does not exists into the cart, default 1 quantity will be added as we set 'quantity ... default=1' in our model, 
        # else item already exists into the cart, add new quantity
        item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            item.quantity += int(quantity)
            item.save()

        # Put the cart inside the serializer and send response
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)


# <--- Increase, Decrease Items or Delete the Cart --->
class ManageCartItemView(APIView):
    
    permission_classes = [IsAuthenticated]

    # Update the Item Quantity
    def patch(self, request, item_id):

        # 'change' should contain either +1 or -1
        if 'change' not in request.data: 
            return Response({"error":"'change' value is required!"})
        
        change = int(request.data.get('change'))
        
        item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
        product = item.product

        if change > 0:
            if item.quantity+change > product.product_stock:
                return Response ({"error":"Not Enough Stock"})
            
        new_quantity = item.quantity + change 

        if new_quantity <= 0 :
            item.delete()
            return Response({"succss":"Item Removed"})
        
        item.quantity = new_quantity
        item.save()

        serializer = CartItemSerializer(item)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


    # Delete the Item from Cart
    def delete(self, request, item_id):

        item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)