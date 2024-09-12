from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Product, Restaurant, Cart, Order, Payment
from .forms import ProductForm
from django.urls import reverse_lazy
# Products
class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'

class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'

class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'store/product_form.html'
    success_url = reverse_lazy('product_list')

class ProductUpdateView(UpdateView):
    model = Product
    fields = ['name', 'description', 'price', 'is_available', 'restaurant']
    template_name = 'store/product_form.html'

class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'product_confirm_delete.html'
    success_url = '/products/'

# Restaurants
class RestaurantListView(ListView):
    model = Restaurant
    template_name = 'restaurant_list.html'

class RestaurantDetailView(DetailView):
    model = Restaurant
    template_name = 'restaurant_detail.html'

# Carts
class CartListView(ListView):
    model = Cart
    template_name = 'cart_list.html'

class CartDetailView(DetailView):
    model = Cart
    template_name = 'cart_detail.html'

class CartCreateView(CreateView):
    model = Cart
    fields = ['restaurant']
    template_name = 'cart_form.html'

# Orders
class OrderListView(ListView):
    model = Order
    template_name = 'order_list.html'

class OrderDetailView(DetailView):
    model = Order
    template_name = 'order_detail.html'

# Payments
class PaymentListView(ListView):
    model = Payment
    template_name = 'payment_list.html'

class PaymentDetailView(DetailView):
    model = Payment
    template_name = 'payment_detail.html'
