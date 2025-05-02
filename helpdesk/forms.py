""" helpdesk/forms.py """
from django import forms
from django.forms import ModelForm

from .models import Ticket, HelpTopic, TicketComment, TicketAttachment, Tasks, Agents

# opção para habilitar o envio de múltiplos arquivos
# https://stackoverflow.com/questions/77212709/django-clearablefileinput-does-not-support-uploading-multiple-files-error
class MultipleFileInput(forms.ClearableFileInput):
    """
    Custom file input widget that allows multiple file uploads.
    """
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('widget', MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial = ...):
        single_file_clean = super().clean

        if isinstance(data, (list, tuple)):
            result = [single_file_clean(dta, initial) for dta in data]
        else:
            result = single_file_clean(data, initial)
        return result

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

class TicketAttachmentForm(ModelForm):
    """
    Form for adding attachments to tickets.
    """
    files = MultipleFileField(
        label='Select files',
        help_text='Select files to upload.',
        required=False,
        widget=MultipleFileInput(attrs={'class': 'form-control', 'multiple': True})
    )
    class Meta:
        model = TicketAttachment
        fields = ['files']

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
        fields = ['task_name', 'description', 'ticket', 'priority', 'assigned_to', 'due_date']
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
            'ticket': forms.Select(attrs={'class': 'form-select', 'aria-label': 'Default select example'}),
            'priority': forms.Select(attrs={'class': 'form-select', 'aria-label': 'Default select example'}),
            'assigned_to': forms.Select(attrs={'class': 'form-select', 'aria-label': 'Default select example'}),
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control w-50'}),
        }

class TaskCommentForm(ModelForm):
    """
    Form for adding comments to tasks.
    """
    class Meta:
        model = TicketComment
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': "Leave a comment here",
                'id':"comment",
                'style':"resize: none; height: 200px;"
                }
            ),
        }