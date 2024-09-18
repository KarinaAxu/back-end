from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    avatar = models.ImageField(upload_to='user/', null=True, blank=True, max_length=2000)
    bio = models.TextField(max_length=2000, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', blank=True, null=True)
    restaurants = models.ForeignKey('store.Restaurant', on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def __str__(self):
        return f'{self.id} {self.owner.first_name} {self.owner.last_name}'

class ResetPassword(models.Model):
    email = models.EmailField(max_length=255)
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Reset Password'
        verbose_name_plural = 'Reset Passwords'

    def __str__(self):
        return f'{self.id} {self.email} {self.token} {self.created_at}'
