from django.db.models.signals import pre_save, post_save, pre_delete, post_delete
from django.dispatch import receiver
from django.utils import timezone

from .models import Ticket, TicketComment, Tasks
from django.core.exceptions import ValidationError

# @receiver(pre_save, sender=Ticket)
# def validate_due_date(sender, instance: Ticket, **kwargs):
#     """
#     Validate that the due date is not in the past.
#     """
#     if instance.due_date < timezone.now():
#         raise ValidationError("Due date cannot be in the past.")

# @receiver(post_delete, sender=Tasks)
# def send_task_log_info_post_delete(sender, instance:Tasks, **kwargs):
#     import logging

#     logger = logging.getLogger(__name__)
#     logger.info(f'Task Delete: {instance.task_name}')
