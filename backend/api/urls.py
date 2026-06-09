from django.urls import path
from users import views as UserViews
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from products import views as ProductViews
from carts import views as CartViews
from orders import views as OrderViews


urlpatterns = [
    # Registration API
    path('register/', UserViews.RegisterView.as_view()),

    # User Profile API
    path('profile/', UserViews.ProfileView.as_view()),

    # Product API
    path('products/', ProductViews.ProductListView.as_view()),

    # Product Detail API
    path('products/<int:pk>/', ProductViews.ProductDetailView.as_view()),

    # Category API
    path('category/', ProductViews.CategoryListView.as_view()),

    # Cart API
    path('cart/', CartViews.CartListView.as_view()),

    # Add to Cart API
    path('cart/add/', CartViews.AddToCartView.as_view()),

    # Manage Cart API
    path('cart/items/<int:item_id>/', CartViews.ManageCartItemView.as_view()),

    # Order Placement API
    path('orders/place/', OrderViews.PlaceOrderView.as_view()),
    
    # Order List API
    path('orders/', OrderViews.MyOrdersView.as_view()),

    # Order Detail API
    path('orders/<int:order_id>', OrderViews.OrderDetailView.as_view()),

    # <--- Third Party APIS --->
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
