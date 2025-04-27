""" helpdesk URL Configuration"""
from django.urls import path
from . import views

urlpatterns = [
    # landpage do helpdesk
    path('', views.index, name='index'),
    # admin page do helpdesk
    path('admin_page/', views.admin_page, name='admin_page'),
    # para criar um novo ticket
    path('ticket/new/', views.create_new_ticket, name='create_new_ticket'),
    # para verificar o estado do ticket
    path('ticket/status/', views.check_ticket_status, name='check_ticket_status'),
    # criar um novo topico de ajuda
    path('help_topic/new/', views.create_help_topic, name='create_help_topic'),
    # path('ticket/<int:ticket_id>/', views.ticket_detail, name='ticket_detail'),
    # path('ticket/<int:ticket_id>/edit/', views.edit_ticket, name='edit_ticket'),
    # path('ticket/<int:ticket_id>/delete/', views.delete_ticket, name='delete_ticket'),
]