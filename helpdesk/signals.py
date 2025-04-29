from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver
from django.utils import timezone

from .models import Ticket, TicketComment
from django.core.exceptions import ValidationError

@receiver(pre_save, sender=Ticket)
def set_ticket_priority(sender, instance, **kwargs):
    """
    Set the ticket priority based on the assigned agent's priority level.
    """
    if instance.help_topic == 'urgent':
        instance.priority = 'urgent'
    elif instance.help_topic == 'high':
        instance.priority = 'high'
    elif instance.help_topic == 'medium':
        instance.priority = 'medium'
    else:
        # Default to low priority if no specific topic is matched
        instance.priority = 'low'

def validate_due_date(value):
    """
    Validate that the due date is not in the past.
    """
    if value < timezone.now():
        raise ValidationError("Due date cannot be in the past.")
