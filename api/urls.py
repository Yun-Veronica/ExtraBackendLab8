from django.urls import path
from .views import *


urlpatterns = [
    path('products', ProductListAPIView.as_view(), name='product-list'),
    path('products/<int:product_id>/buy', ProductBuyView.as_view(), name='product-buy'),
    path('products/<int:product_id>', ProductDetailView.as_view(), name='product-detail'),

    path('login', UserLoginView.as_view(), name='login'),
    path('register', UserRegisterView.as_view(), name='register'),
    path('user/<int:user_id>/orders', UserOrderListView.as_view(), name='user-order-list'),

    path('categories', CategoryListView.as_view(), name='category-list'),
    path('categories/<int:category_id>/products', CategoryProductListView.as_view(), name='category-product-list'),
]


