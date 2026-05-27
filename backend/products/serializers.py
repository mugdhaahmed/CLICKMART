from rest_framework import serializers
from .models import Category, Product


# <--- Product Serializer --->
class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = "__all__"
        

# <--- Category Serializer --->
class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"


