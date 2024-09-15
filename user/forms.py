from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Profile


class LoginForm(forms.Form):
    username = forms.CharField(required=True, min_length=2, max_length=25,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(required=True, min_length=6, max_length=20,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

class RegisterForm(forms.ModelForm):
    repeat_password = forms.CharField(required=True, min_length=6, max_length=20,
                                      widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Repeat your password'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
        }

    def clean_repeat_password(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('repeat_password')
        if password1 and password2 and password1 != password2:
            raise ValidationError('Passwords do not match')
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(required=True, min_length=4, max_length=200,
                             widget=forms.TextInput({'class': 'form-control', 'type': 'email'}))


class ResetPasswordForm(forms.Form):
    password = forms.CharField(required=True, min_length=8, max_length=20,
                               widget=forms.PasswordInput({'class': 'form-control', 'type': 'password',
                                                           'placeholder': 'Enter your password'}))
    repeat_password = forms.CharField(required=True, min_length=8, max_length=20,
                                      widget=forms.PasswordInput({'class': 'form-control', 'type': 'password',
                                                                  'placeholder': 'Repeat your password'}))

    def clean_repeat_password(self):
        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("repeat_password")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'avatar']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter your bio'}),
        }