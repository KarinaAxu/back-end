from django.contrib import admin
from django.core.exceptions import ValidationError
from . import models

class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'restaurant', 'created_at', 'updated_at')
    list_filter = ('created_at', 'restaurant')
    search_fields = ('user__username',)

    actions = ['create_order']

    def create_order(self, request, queryset):
        for cart in queryset:
            if cart.cartitem_set.exists():
                order = models.Order.objects.create(
                    user=cart.user,
                    courier=None,
                    delivery_fee=4.95,
                    status='pending'
                )
                for cart_item in cart.cartitem_set.all():
                    models.OrderItem.objects.create(
                        order=order,
                        cart_item=cart_item,
                        quantity=cart_item.quantity
                    )
                order.save()
                cart.cartitem_set.all().delete()
                self.message_user(request, f'Order created for cart {cart.id}')
            else:
                self.message_user(request, f'Cart {cart.id} is empty', level='warning')

    create_order.short_description = 'Create order for selected carts'

class CartItemAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        try:
            obj.clean()
        except ValidationError as e:
            form.add_error(None, e.message)
            return
        super().save_model(request, obj, form, change)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_amount', 'courier', 'delivery_fee', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'courier', 'created_at')
    search_fields = ('user__username',)


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'get_total_quantity', 'get_total_price', 'created_at')
    list_filter = ('order',)
    search_fields = ('cart_items__dish__name',)

    def get_total_quantity(self, obj):
        return obj.get_total_quantity()

    def get_total_price(self, obj):
        return obj.get_total_price()

admin.site.register(models.Dish)
admin.site.register(models.Restaurant)
admin.site.register(models.Address)
admin.site.register(models.Payment)
admin.site.register(models.Courier)

admin.site.register(models.Cart, CartAdmin)
admin.site.register(models.CartItem, CartItemAdmin)
admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.OrderItem, OrderItemAdmin)
