""" users/models.py """
from django import forms
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.translation import gettext_lazy as _

class UserRegistrationForm(UserCreationForm):
    """
    Form for user registration.
    """
    # email = forms.EmailField(required=True, label=_("Email"), max_length=254, help_text=_("Required. Inform a valid email address."))
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('John.doe')}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'type': "email", 'id':"InputEmail", 'placeholder': "example@company.com", 'aria-describedby': "emailHelp"}),
        }
