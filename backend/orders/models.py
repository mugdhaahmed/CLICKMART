from django.db import models
from django.contrib.auth import get_user_model
from products.models import Product
from typing import TYPE_CHECKING  

User = get_user_model()

# <--- Order Model --->
class Order(models.Model):

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('DELIVERED', 'Delivered')
    ]

    user = models.ForeignKey(User, on_delete=models.PROTECT)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=6, decimal_places=2)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    address = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=12, blank=True, null=True)
    city = models.CharField(max_length=20, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    zip_code = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    if TYPE_CHECKING:
        from .models import Order
        id: models.QuerySet["Order"]

    def __str__(self):
        return f"Order #{self.id} - {self.user.email}"



# <--- Order Item Model --->
class OrderItem(models.Model):

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveBigIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.product_name} x {self.quantity}"
