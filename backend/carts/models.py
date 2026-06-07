from django.db import models
from django.contrib.auth import get_user_model
from products.models import Product
from decimal import Decimal
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .models import CartItem


User = get_user_model()

# <--- Cart Model --->
class Cart(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cart_created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email
    
    if TYPE_CHECKING:
        cart_items: models.QuerySet["CartItem"]

    # Subtotal Helper Function
    @property
    def subtotal(self): # cart.subtotal
        subtotal = Decimal("0.00")
        for item in self.cart_items.all():
            subtotal += item.product.product_price * item.quantity
        return subtotal
    
    # Tax Amount Helper Function
    @property
    def tax_amount(self): # cart.tax_amount
        tax = Decimal("0.00")
        for item in self.cart_items.all():
            tax += (item.product.product_price * item.quantity * Decimal(item.product.product_tax_percentage / Decimal("100.00")))
        return tax
    
    # Grand Total Helper Function
    @property
    def grand_total(self): # cart.grand_total
        grand_total = self.subtotal + self.tax_amount
        return grand_total.quantize(Decimal("0.00"))

    

# <--- Cart Items Model --->
class CartItem(models.Model):
    
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"({self.product.product_name} x {self.quantity})"
    
    # Total Price Helper Function
    @property
    def total_price(self): # cart_item.total_price
        total_price = self.product.product_price * self.quantity
        return total_price
