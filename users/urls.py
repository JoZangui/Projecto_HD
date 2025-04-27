""" users URL Configuration """
from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    # Registration page
    path('register/', views.user_registration, name='user_registration'),
    # Success page after registration
    path('success/', views.success, name='success'),
    #login
    path('login/', views.user_login, name='login'),
    #logout page
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
]