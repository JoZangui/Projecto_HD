""" users/models.py """
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class Agents(models.Model):
    """
    Model for agents.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='agent')
    # Add any additional fields you need for the agent here
    privilege_level = models.CharField(max_length=20, choices=[
        ('admin', 'Admin'),
        ('agente', 'Agente'),
        ('suporte', 'Suporte'),
    ], default='user', help_text=_("Select the privilege level for the agent."))  # Example field for privilege level

    def __str__(self):
        return self.user.username  # or any other field you want to display
    
    class Meta:
        verbose_name = _('Agent')
        verbose_name_plural = _('Agents')
        ordering = ['user__username']
