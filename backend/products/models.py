from django.db import models
from decimal import Decimal


# <--- Category Model --->
class Category(models.Model):

    category_name = models.CharField(max_length=25)
    category_description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.category_name


# <--- Product Model --->
class Product(models.Model):

    product_name = models.CharField(max_length=100)
    product_description = models.TextField()
    product_category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True)
    product_image = models.ImageField(upload_to='products/', blank=True, null=True)
    product_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal(0.00))
    product_stock = models.PositiveIntegerField()
    product_tax_percentage = models.DecimalField(max_digits=3, decimal_places=2, default=Decimal(0.00))
    product_is_active = models.BooleanField(default=True)
    product_created_at = models.DateTimeField(auto_now_add=True)
    product_updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.product_name

