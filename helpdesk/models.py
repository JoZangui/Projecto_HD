from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError

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
    assigned_to = models.ForeignKey(User, null=True, blank=True, related_name='assigned_tickets', on_delete=models.SET_NULL)  # User assigned to resolve the ticket
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    due_date = models.DateTimeField(null=True, blank=True)  # Optional due date for resolution
    status = models.CharField(max_length=20, choices=[
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('closed', 'Closed')
    ], default='open')  # e.g., open, in_progress, closed

    def __str__(self):
        return f'Ticket: {self.issue_summary}; Criado por: {self.user.username}'

    class Meta:
        verbose_name_plural = "Tickets" # Plural name for the model in admin interface

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
