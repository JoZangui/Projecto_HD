import datetime

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError

from users.models import Agents

class HelpTopic(models.Model):
    """
    Model representing a help topic for categorizing tickets.
    """
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Topicos de Ajuda"  # Plural name for the model in admin interface

class Ticket(models.Model):
    """
    Model representing a support ticket.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    help_topic = models.ForeignKey(HelpTopic, on_delete=models.CASCADE)  # e.g., billing, technical, general inquiry
    issue_summary = models.CharField(max_length=200)
    description = models.TextField()
    priority = models.CharField(max_length=20, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent')
    ], default='medium') # essa prioridade do ticket vai ser preenchida de forma com signals
    assigned_to = models.ForeignKey(Agents, null=True, blank=True, related_name='assigned_tickets', on_delete=models.SET_NULL)  # User assigned to resolve the ticket
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    due_date = models.DateTimeField(null=True, blank=True)  # Optional due date for resolution
    status = models.CharField(max_length=20, choices=[
        ('aberto', 'Aberto'),
        ('em_progresso', 'Em Progresso'),
        ('fechado', 'Fechado')
    ], default='open')  # e.g., open, in_progress, closed

    def __str__(self):
        return f'{self.issue_summary}; Criado por: {self.user.username}'

    class Meta:
        verbose_name_plural = "Tickets" # Plural name for the model in admin interface

    def clean(self):
        if self.due_date and self.due_date < timezone.now():
            raise ValidationError("Due date cannot be in the past.")

class TicketComment(models.Model):
    """
    Model representing a comment on a support ticket.
    """
    ticket = models.ForeignKey(Ticket, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.ticket.issue_summary}"

    class Meta:
        verbose_name_plural = "Comentarios de Tickets"

class TicketAttachment(models.Model):
    """
    Model representing an attachment to a support ticket.
    """
    ticket = models.ForeignKey(Ticket, related_name='attachments', on_delete=models.CASCADE)
    file = models.FileField(upload_to='ticket_attachments/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Attachment for {self.ticket.issue_summary}"
    
    class Meta:
        verbose_name_plural = "Anexos de Tickets"

class Tasks(models.Model):
    """
    Model representing a task related to a support ticket.
    """
    ticket = models.ForeignKey(Ticket, related_name='tasks', on_delete=models.CASCADE)
    task_name = models.CharField(max_length=100, null=True, blank=True)
    assigned_to = models.ForeignKey(Agents, null=True, blank=True, related_name='assigned_tasks', on_delete=models.SET_NULL)
    description = models.TextField()
    due_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed')
    ], default='not_started')
    priority = models.CharField(max_length=20, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent')
    ], default='medium')
    task_atachments = models.ManyToManyField(TicketAttachment, blank=True, related_name='task_attachments')
    created_by = models.ForeignKey(Agents, on_delete=models.CASCADE, related_name='created_tickets', default=1)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=timezone.now)

    def __str__(self):
        return f"Task for {self.ticket.issue_summary}"
    
    class Meta:
        verbose_name_plural = "Tarefas"

    def clean(self):
        """
        Custom validation to ensure the due date is not in the past.
        """
        if self.due_date and self.due_date < datetime.date.today():
            raise ValidationError("Data de entrega não pode estar no passado.")


class TaskAttachment(models.Model):
    """
    Model representing an attachment to a task related to a support ticket.
    """
    task = models.ForeignKey(Tasks, related_name='attachments', on_delete=models.CASCADE)
    file = models.FileField(upload_to='task_attachments/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Attachment for task {self.task.description}"
    
    class Meta:
        verbose_name_plural = "Anexos de Tarefas"

class TaskComments(models.Model):
    """
    Model representing a comment on a task related to a support ticket.
    """
    task = models.ForeignKey(Tasks, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on task {self.task.description}"
    
    class Meta:
        verbose_name_plural = "Comentarios de Tarefas"

# Avaliar mais tarde
class TasksHistory(models.Model):
    """
    Model representing the history of tasks related to a support ticket.
    """
    task = models.ForeignKey(Tasks, related_name='history', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed')
    ])
    changed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Task history for {self.task.ticket.issue_summary} to {self.status} at {self.changed_at}"
    
    class Meta:
        verbose_name_plural = "Historico de Tarefas"

class TicketStatusHistory(models.Model):
    """
    Model representing the history of status changes for a support ticket.
    """
    ticket = models.ForeignKey(Ticket, related_name='status_history', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[
        ('aberto', 'Aberto'),
        ('em_progresso', 'Em Progresso'),
        ('fechado', 'Fechado')
    ])
    changed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Status change for {self.ticket.issue_summary} to {self.status} at {self.changed_at}"
    
    class Meta:
        verbose_name_plural = "Historico de Status de Tickets"

        ordering = ['-changed_at']
        # Orders the history by the most recent change first
        # This is useful for displaying the history in reverse chronological order.
        # You can also add unique constraints or other Meta options as needed.
        # For example, you might want to ensure that each ticket can only have one status change at a time.
        # This ensures that the combination of ticket and changed_at is unique, preventing duplicate entries.
        # You can also add indexes for faster querying if needed.
        unique_together = ('ticket', 'changed_at')

class TicketPriorityHistory(models.Model):
    """
    Model representing the history of priority changes for a support ticket.
    """
    ticket = models.ForeignKey(Ticket, related_name='priority_history', on_delete=models.CASCADE)
    priority = models.CharField(max_length=20, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent')
    ])
    changed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Priority change for {self.ticket.issue_summary} to {self.priority} at {self.changed_at}"
    
    class Meta:
        verbose_name_plural = "Historico de Prioridade de Tickets"

        ordering = ['-changed_at']
        unique_together = ('ticket', 'changed_at')