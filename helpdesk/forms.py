from django import forms
from django.forms import ModelForm

from .models import Ticket, HelpTopic, TicketComment, TicketAttachment

class TicketForm(ModelForm):
    """
    Form for creating and updating tickets.
    """
    class Meta:
        model = Ticket
        fields = ['user', 'help_topic', 'issue_summary', 'description', 'due_date']
        widgets = {
            # user
            'user': forms.Select(attrs={'class': 'form-select', 'aria-label': 'Default select example'}),
            # help_topic
            'help_topic': forms.Select(attrs={'class': 'form-select', 'aria-label': 'Default select example'}),
            # issue_summary
            'issue_summary': forms.TextInput(attrs={'class': 'form-control', 'type': 'text', 'aria-label': 'form-control-lg example', 'placeholder': 'Summarize the issue'}),
            # description
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': "Leave a comment here", 'id': "floatingTextarea2", 'style': "height: 200px; resize: none;"}),
            # due_date
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }

class TicketCommentForm(ModelForm):
    """
    Form for adding comments to tickets.
    """
    class Meta:
        model = TicketComment
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'cols': 40}),
        }

class HelpTopicForm(ModelForm):
    """
    Form for creating and updating help topics.
    """
    class Meta:
        model = HelpTopic
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'cols': 40}),
        }
