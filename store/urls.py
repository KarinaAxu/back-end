from django.urls import path
from .views import (
    ProductListView, ProductDetailView, ProductCreateView,
    ProductUpdateView, ProductDeleteView,
    RestaurantListView, RestaurantDetailView,
    RestaurantCreateView, RestaurantDeleteView, RestaurantUpdateView,
    CartListView, CartDetailView,
    OrderListView, OrderDetailView,
    PaymentListView, PaymentDetailView
)

urlpatterns = [
    # Products
    path('products/', ProductListView.as_view(), name='product_list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('products/new/', ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/edit/', ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),

    # Restaurants
    path('restaurants/', RestaurantListView.as_view(), name='restaurant_list'),
    path('restaurants/<int:pk>/', RestaurantDetailView.as_view(), name='restaurant_detail'),
    path('restaurants/new/', RestaurantCreateView.as_view(), name='restaurant_create'),
    path('restaurants/<int:pk>/edit/', RestaurantUpdateView.as_view(), name='restaurant_update'),
    path('restaurants/<int:pk>/delete/', RestaurantDeleteView.as_view(), name='restaurant_delete'),

    # Carts
    path('carts/', CartListView.as_view(), name='cart_list'),
    path('carts/<int:pk>/', CartDetailView.as_view(), name='cart_detail'),

    # Orders
    path('orders/', OrderListView.as_view(), name='order_list'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),

    # Payments
    path('payments/', PaymentListView.as_view(), name='payment_list'),
    path('payments/<int:pk>/', PaymentDetailView.as_view(), name='payment_detail'),
]
