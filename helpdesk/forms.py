from django import forms
from django.forms import ModelForm

from .models import Ticket, HelpTopic, TicketComment, TicketAttachment, Tasks, Agents

class TicketForm(ModelForm):
    """
    Form for creating and updating tickets.
    """
    class Meta:
        model = Ticket
        fields = ['help_topic', 'issue_summary', 'description', 'due_date']
        widgets = {
            # help_topic
            'help_topic': forms.Select(attrs={'class': 'form-select', 'aria-label': 'Default select example'}),
            # issue_summary
            'issue_summary': forms.TextInput(attrs={'class': 'form-control', 'type': 'text', 'aria-label': 'form-control-lg example', 'placeholder': 'Assunto'}),
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
            'comment': forms.Textarea(attrs={'class': 'form-control', 'placeholder': "Leave a comment here", 'id':"comment",'style':"resize: none; height: 200px;"}),
        }

class HelpTopicForm(ModelForm):
    """
    Form for creating and updating help topics.
    """
    class Meta:
        model = HelpTopic
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the name of the help topic'}),
        }

class TasksForm(ModelForm):
    """
    Form for creating and updating tasks.
    """
    class Meta:
        model = Tasks
        fields = ['task_name', 'description', 'priority', 'due_date']
        widgets = {
            'task_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the name of the task'}),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': "Leave a comment here",
                    'id':"comment",
                    'style':"resize: none; height: 200px;"
                }
            ),
            'priority': forms.Select(attrs={'class': 'form-select', 'aria-label': 'Default select example'}),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }
