""" helpdesk URL Configuration"""
from django.urls import path
from . import views

urlpatterns = [
    # landpage do helpdesk
    path('', views.index, name='index'),
    # admin page do helpdesk
    path('admin_page/', views.admin_page, name='admin_page'),

    # ---------- Tickets urls ----------
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

    # ---------- Tasks urls ----------
    # criar nova tarefa
    path('task/new/', views.create_new_task, name='create_new_task'),
    # detalhes da tarefa
    path('task/<int:task_id>/', views.task_detail, name='task_detail'),
    # editar tarefa
    path('task/<int:task_id>/edit/', views.edit_task, name='edit_task'),
    # deletar tarefa
    path('task/<int:task_id>/delete/', views.delete_task, name='delete_task'),
    # adicionar comentario ao tarefa
    path('task/<int:task_id>/comment/', views.create_task_comment, name='create_task_comment'),
    # atribuir tarefa a um agente
    path('task/<int:task_id>/assign/', views.assign_task, name='assign_task'),
    # mudar o estado da tarefa
    path('task/<int:task_id>/change_status/', views.change_task_status, name='change_task_status'),
]