from django.urls import path
from .views import login_page, register_page, logout, profile_page, forgot_password, reset_password
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login/', login_page, name='login'),
    path('register/', register_page, name='register'),
    path('logout/', logout, name='logout'),
    path('settings/', profile_page, name='settings_page'),
    path('forgot-password/', forgot_password, name='forgot_password'),
    path('reset-password/<slug:token>', reset_password, name='reset_password'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
