from django.contrib import admin
from orders.models import Order, OrderItem


# <--- Modify Admin Panel with Tabuler Inline --->
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    readonly_fields = ['product','quantity','price','total_price']

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]


admin.site.register(Order, OrderAdmin)
# admin.site.register(OrderItem)
