""" users/models.py """
from django import forms
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.translation import gettext_lazy as _

from .models import Agents

class UserRegistrationForm(UserCreationForm):
    """
    Form for user registration.
    """
    # email = forms.EmailField(required=True, label=_("Email"), max_length=254, help_text=_("Required. Inform a valid email address."))
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('John.doe')}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('John')}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Doe')}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'type': "email", 'id':"InputEmail", 'placeholder': "example@company.com", 'aria-describedby': "emailHelp"}),
        }

class AgentRegistrationForm(forms.ModelForm):
    """
    Form for agent registration.
    """
    class Meta:
        model = Agents
        fields = ('user', 'privilege_level')
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'privilege_level': forms.Select(attrs={'class': 'form-control'}),
        }

    # Filtrar usuários no campo de seleção de usuário para mostrar apenas aqueles que não são agentes
    def __init__(self, *args, **kwargs):
        # Filtra os usuários que não estão cadastrados como agentes
        super(AgentRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.exclude(id__in=Agents.objects.values_list('user', flat=True))
