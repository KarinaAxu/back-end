from django import forms
from .models import Product, Restaurant


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'is_available', 'restaurants']
        widgets = {
            'restaurants': forms.SelectMultiple({'class': 'form-select'})
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        self.fields['price'].widget.attrs.update({'class': 'form-control'})
        self.fields['is_available'].widget.attrs.update({'class': 'form-check-input'})
        self.fields['restaurants'].widget.attrs.update({'class': 'form-select'})

    def save(self, commit=True):
        product = super().save(commit=False)
        if self.user:
            product.created_by = self.user
        if commit:
            product.save()
            self.save_m2m()
        return product

class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['name', 'address', 'phone', 'email']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['address'].widget.attrs.update({'class': 'form-control'})
        self.fields['phone'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})

    def save(self, commit=True):
        restaurant = super().save(commit=False)
        if self.user:
            restaurant.owner = self.user
        if commit:
            restaurant.save()
        return restaurant
