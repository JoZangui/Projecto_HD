""" helpdesk URL Configuration"""
from django.urls import path
from . import views

urlpatterns = [
    # landpage do helpdesk
    path('', views.index, name='index'),
    # admin page do helpdesk
    path('admin_page/', views.admin_page, name='admin_page'),
    # lista de tickets
    path('ticket_list/', views.ticket_list, name='ticket_list'),
    # para criar um novo ticket
    path('ticket/new/', views.create_new_ticket, name='create_new_ticket'),
    # detalhes do ticket
    path('ticket/<int:ticket_id>/', views.ticket_detail, name='ticket_detail'),
    # para verificar o estado do ticket
    path('ticket/status/', views.check_ticket, name='check_ticket'),
    # mudar o estado do ticket
    path('ticket/new_status/', views.change_ticket_status, name='change_ticket_status'),
    # criar um novo topico de ajuda
    path('help_topic/new/', views.create_help_topic, name='create_help_topic'),
    # atribuir ticket a um agente
    path('ticket/<int:ticket_id>/assign/', views.assign_ticket, name='assign_ticket'),
    # editar ticket
    path('ticket/<int:ticket_id>/edit/', views.edit_ticket, name='edit_ticket'),
    # deletar ticket
    path('ticket/<int:ticket_id>/delete/', views.delete_ticket, name='delete_ticket'),
    # task list
    path('task_list/', views.task_list, name='task_list'),
    # criar nova tarefa
]