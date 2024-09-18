from django.urls import path
from .views import (
    DishListView, DishDetailView, DishCreateView,
    DishUpdateView, DishDeleteView,
    RestaurantListView, RestaurantDetailView,
    RestaurantCreateView, RestaurantDeleteView, RestaurantUpdateView,
    CartListView, CartDetailView,
    OrderListView, OrderDetailView,
    PaymentListView, PaymentDetailView, OrderCreate
)

urlpatterns = [
    # Dishs
    path('dish/', DishListView.as_view(), name='dish_list'),
    path('dish/<int:pk>/', DishDetailView.as_view(), name='dish_detail'),
    path('dish/new/', DishCreateView.as_view(), name='dish_create'),
    path('dish/<int:pk>/edit/', DishUpdateView.as_view(), name='dish_update'),
    path('dish/<int:pk>/delete/', DishDeleteView.as_view(), name='dish_delete'),

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
    path('order/create/', OrderCreate, name='order_create'),

    # Payments
    path('payments/', PaymentListView.as_view(), name='payment_list'),
    path('payments/<int:pk>/', PaymentDetailView.as_view(), name='payment_detail'),
]
