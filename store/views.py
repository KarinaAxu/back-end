from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from .models import Product, Restaurant, Cart, Order, Payment
from .forms import ProductForm, RestaurantForm

class ProductListView(ListView):
    model = Product
    template_name = 'store/product_list.html'
    paginate_by = 10

class ProductDetailView(DetailView):
    model = Product
    template_name = 'store/product_detail.html'

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'store/product_form.html'
    success_url = reverse_lazy('product_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'store/product_form.html'

    def get_object(self):
        product = get_object_or_404(Product, pk=self.kwargs['pk'])
        if product.created_by != self.request.user:
            raise PermissionDenied
        return product

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'store/product_confirm_delete.html'
    success_url = reverse_lazy('product_list')

    def get_object(self):
        product = get_object_or_404(Product, pk=self.kwargs['pk'])
        if product.created_by != self.request.user:
            raise PermissionDenied
        return product

class RestaurantListView(ListView):
    model = Restaurant
    template_name = 'store/restaurant_list.html'

class RestaurantDetailView(DetailView):
    model = Restaurant
    template_name = 'store/restaurant_detail.html'

class RestaurantCreateView(LoginRequiredMixin, CreateView):
    model = Restaurant
    form_class = RestaurantForm
    template_name = 'store/restaurant_form.html'
    success_url = reverse_lazy('restaurant_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class RestaurantUpdateView(LoginRequiredMixin, UpdateView):
    model = Restaurant
    form_class = RestaurantForm
    template_name = 'store/restaurant_form.html'

    def get_object(self):
        restaurant = get_object_or_404(Restaurant, pk=self.kwargs['pk'])
        if restaurant.owner != self.request.user:
            raise PermissionDenied
        return restaurant

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class RestaurantDeleteView(LoginRequiredMixin, DeleteView):
    model = Restaurant
    template_name = 'store/restaurant_confirm_delete.html'
    success_url = reverse_lazy('restaurant_list')

    def get_object(self):
        restaurant = get_object_or_404(Restaurant, pk=self.kwargs['pk'])
        if restaurant.owner != self.request.user:
            raise PermissionDenied
        return restaurant

class CartListView(ListView):
    model = Cart
    template_name = 'store/cart_list.html'

class CartDetailView(DetailView):
    model = Cart
    template_name = 'store/cart_detail.html'

class OrderListView(ListView):
    model = Order
    template_name = 'store/order_list.html'

class OrderDetailView(DetailView):
    model = Order
    template_name = 'store/order_detail.html'

class PaymentListView(ListView):
    model = Payment
    template_name = 'store/payment_list.html'

class PaymentDetailView(DetailView):
    model = Payment
    template_name = 'store/payment_detail.html'
