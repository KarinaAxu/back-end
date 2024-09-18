from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from .models import Dish, Restaurant, Cart, Order, Payment, CartItem, OrderItem
from .forms import DishForm, RestaurantForm

class DishListView(ListView):
    model = Dish
    template_name = 'store/dish_list.html'
    paginate_by = 10

class DishDetailView(DetailView):
    model = Dish
    template_name = 'store/dish_detail.html'

class DishCreateView(LoginRequiredMixin, CreateView):
    model = Dish
    form_class = DishForm
    template_name = 'store/dish_form.html'
    success_url = reverse_lazy('dish_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class DishUpdateView(LoginRequiredMixin, UpdateView):
    model = Dish
    form_class = DishForm
    template_name = 'store/dish_form.html'
    success_url = reverse_lazy('dish_list')

    def get_object(self):
        dish = get_object_or_404(Dish, pk=self.kwargs['pk'])
        if dish.created_by != self.request.user:
            raise PermissionDenied
        return dish

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class DishDeleteView(LoginRequiredMixin, DeleteView):
    model = Dish
    template_name = 'store/dish_confirm_delete.html'
    success_url = reverse_lazy('dish_list')

    def get_object(self):
        dish = get_object_or_404(Dish, pk=self.kwargs['pk'])
        if dish.created_by != self.request.user:
            raise PermissionDenied
        return dish

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
    success_url = reverse_lazy('restaurant_list')

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


def CartAdd(request, dish_id):
    dish = get_object_or_404(Dish, id=dish_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    if cart.restaurants and dish.restaurants.exclude(id=cart.restaurants.id).exists():
        return redirect('cart_list')

    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, dish=dish)

    if not item_created:
        cart_item.quantity += 1
    else:
        cart_item.quantity = 1

    cart_item.save()

    return redirect('cart_list')


def CartView(request):
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        return redirect('cart_list')

    cart_items = cart.cartitem_set.all()
    total_items = cart.get_total_items()
    total_cost = cart.get_total_cost()

    context = {
        'cart': cart,
        'cart_items': cart_items,
        'total_items': total_items,
        'total_cost': total_cost,
    }

    return render(request, 'store/cart_list.html', context)

class OrderListView(ListView):
    model = Order
    template_name = 'store/order_list.html'

class OrderDetailView(DetailView):
    model = Order
    template_name = 'store/order_detail.html'

def OrderCreate(request):
    cart = Cart.objects.get(user=request.user)
    if not cart.cartitem_set.exists():
        return redirect('cart_list')

    order = Order.objects.create(user=request.user, total_amount=0)

    order_item = OrderItem.objects.create(order=order)

    for cart_item in cart.cartitem_set.all():
        order_item.cart_items.add(cart_item)

    order_item.save()
    order.calculate_total()
    order.save()

    cart.cartitem_set.all().delete()

    return redirect('order_list')

class PaymentListView(ListView):
    model = Payment
    template_name = 'store/payment_list.html'

class PaymentDetailView(DetailView):
    model = Payment
    template_name = 'store/payment_detail.html'
