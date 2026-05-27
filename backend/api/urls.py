from django.urls import path
from users import views as UserViews
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from products import views as ProductViews


urlpatterns = [
    # Registration API
    path('register/', UserViews.RegisterView.as_view()),
    # User Profile API
    path('profile/', UserViews.ProfileView.as_view()),
    # Product API
    path('product/', ProductViews.ProductListView.as_view()),
    # Product Detail API
    path('product/<int:pk>', ProductViews.ProductDetailView.as_view()),
    # Category API
    path('category/', ProductViews.CategoryListView.as_view()),

    # <--- Third Party APIS --->
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
