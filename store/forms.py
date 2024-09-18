from django import forms
from .models import Dish, Restaurant


class DishForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = ['name', 'description', 'price', 'restaurants', 'is_available']
        widgets = {
            'restaurants': forms.SelectMultiple({'class': 'form-select'})
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        self.fields['price'].widget.attrs.update({'class': 'form-control'})
        self.fields['restaurants'].widget.attrs.update({'class': 'form-select'})
        self.fields['is_available'].widget.attrs.update({'class': 'form-check-input'})

    def save(self, commit=True):
        dish = super().save(commit=False)
        if self.user:
            dish.created_by = self.user
        if commit:
            dish.save()
            self.save_m2m()
        return dish

class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['name', 'address', 'phone', 'email']
        widgets = {
            'address': forms.SelectMultiple({'class': 'form-select'})
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['address'].widget.attrs.update({'class': 'form-select'})
        self.fields['phone'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})

    def save(self, commit=True):
        restaurant = super().save(commit=False)
        if self.user:
            restaurant.owner = self.user
        if commit:
            restaurant.save()
        return restaurant
