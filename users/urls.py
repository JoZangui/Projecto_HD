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
    # Agent registration page
    path('agent/register/', views.agent_registration, name='agent_registration'),
    # Agent list page
    # path('agent/list/', views.agent_list, name='agent_list'),
    # # Agent detail page
    # path('agent/<int:pk>/', views.agent_detail, name='agent_detail'),
    # # Agent update page
    # path('agent/update/<int:pk>/', views.agent_update, name='agent_update'),
    # # Agent delete page
    # path('agent/delete/<int:pk>/', views.agent_delete, name='agent_delete'),
]