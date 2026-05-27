from rest_framework import generics
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer


# <--- Product List View --->
class ProductListView(generics.ListAPIView):

    queryset = Product.objects.filter(product_is_active=True)
    serializer_class = ProductSerializer


# <--- Product Detail View --->
class ProductDetailView(generics.RetrieveAPIView):

    queryset = Product.objects.filter(product_is_active=True)
    serializer_class = ProductSerializer
    lookup_field = 'pk'


# <--- Product Category View --->
class CategoryListView(generics.ListAPIView):
    
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


