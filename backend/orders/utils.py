from django.core.mail import send_mail
from django.conf import settings


# Send email for order confirmation
def send_order_notification(order):
    send_mail(
        subject=f"Order #{order.id} is received",
        message=f"""
            Hi {order.user.first_name}, greetings from CLICKMART.
            Your order #{order.id} has been placed successfully.
            Total: {order.grand_total} BDT
            Thank you for shopping with us.
            """,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[order.user.email],
        fail_silently=False
    )