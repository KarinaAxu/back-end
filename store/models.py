from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models

class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    address = models.ManyToManyField('Address', related_name='restaurants_add')
    phone = models.CharField(max_length=15, null=True, blank=True, default='7 (777) 777 77')
    email = models.EmailField(max_length=100, default='mega@gmail.com')
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='restaurants', default=1)

    def __str__(self):
        return self.name

class Dish(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    restaurants = models.ManyToManyField('Restaurant', related_name='dish_restaurants')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dishes', default=1)
    is_available = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Dish'
        verbose_name_plural = 'Dishes'

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart {self.id} for {self.user.username}"

    def get_available_dishes(self):
        return Dish.objects.filter(restaurants=self.restaurant)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_total_price(self):
        return self.quantity * self.dish.price

    def clean(self):
        if self.dish.restaurants.first() != self.cart.restaurant:
            raise ValidationError("You can only add dishes from the selected restaurant.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


STATUS_CHOICES = [
    ('active', 'Active'),
    ('inactive', 'Inactive'),
    ('suspended', 'Suspended'),
]
class Courier(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=15, null=True, blank=True, default='7 (777) 777 77')
    vehicle_type = models.CharField(max_length=100, default='bike')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    license_number = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name}, Status: {self.status}" if self.first_name else f"{self.user.first_name}, Status: {self.status}"

STATUS_CHOICES3 = [
        ('pending', 'Pending'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
]

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    courier = models.ForeignKey(Courier, on_delete=models.SET_NULL, null=True)
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=950)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES3, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            super().save(*args, **kwargs)

        self.calculate_total()
        super().save(update_fields=['total_amount'])

    def calculate_total(self):
        total = sum(order_item.get_total_price() for order_item in self.orderitem_set.all())
        total += self.delivery_fee
        self.total_amount = total


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    cart_item = models.ForeignKey(CartItem, on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def get_total_quantity(self):
        return self.cart_item.quantity

    def get_total_price(self):
        return self.cart_item.get_total_price()

    def __str__(self):
        return f"Order: {self.order.id}, Total Quantity: {self.get_total_quantity()}"


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    building_name = models.CharField(max_length=100, blank=True, null=True)
    house_address = models.CharField(max_length=200)
    city = models.CharField(max_length=100, default='Almaty')
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.building_name}" if self.building_name else f"{self.house_address}"

STATUS_CHOICES2 = [
    ('visa', 'VISA Cart'),
    ('kaspi', 'Kaspi QR'),
    ('in cash', 'In Cash'),
]
class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    payment_method = models.CharField(max_length=20, choices=STATUS_CHOICES2, default='in cash')
    status = models.BooleanField(default=False)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment on {self.payment_date.strftime('%Y-%m-%d')}"

    def save(self, *args, **kwargs):
        self.amount = sum(
            item.get_total_price() for item in self.order.orderitem_set.all()
        )
        super().save(*args, **kwargs)
