""" helpdesk/views.py """
import logging

from django.shortcuts import render, HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from .models import Ticket, HelpTopic, TicketComment #, TicketAttachment
from .forms import TicketForm, HelpTopicForm, TicketCommentForm #, TicketAttachmentForm

# Create your views here.
def index(request):
    return render(request, 'helpdesk/index.html')

@login_required
def admin_page(request):
    """ Admin page for helpdesk """
    help_topics = HelpTopic.objects.all()
    tickets = Ticket.objects.all()
    return render(request, 'helpdesk/admin_page.html', {'help_topics': help_topics, 'tickets': tickets})

@login_required
def ticket_list(request):
    """ List all tickets """
    tickets = Ticket.objects.all()
    return render(request, 'helpdesk/ticket_list.html', {'tickets': tickets})

@login_required
def create_new_ticket(request):
    """ Create a new ticket """
    logger = logging.getLogger(__name__)
    
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user  # Assuming the user is logged in
            ticket.save()
            logger.info(f'Ticket created: {ticket.issue_summary} by {request.user.username}')
            # Here you would typically send an email notification or perform other actions
            return HttpResponseRedirect('/helpdesk/ticket/status/')  # Redirect to ticket status page after saving
    else:
        form = TicketForm()
    return render(request, 'helpdesk/new_ticket_form.html', {'form': form})

@login_required
def check_ticket_status(request):
    """ Check the status of a ticket """
    if request.method == 'POST':
        form = HelpTopicForm(request.POST)
        if form.is_valid():
            ticket_id = form.cleaned_data['ticket_id']
            # Here you would typically look up the ticket by ID and get its status
            # For now, we'll just redirect to a dummy ticket detail page
            return HttpResponseRedirect(f'/helpdesk/ticket/{ticket_id}/')
    else:
        form = HelpTopicForm()
    # You might want to include a list of tickets or some other information here
    return render(request, 'helpdesk/check_ticket_status_form.html')

def ticket_detail(request, ticket_id):
    """ View ticket details """
    try:
        ticket = Ticket.objects.get(id=ticket_id)
        comments = TicketComment.objects.filter(ticket=ticket)
    except Ticket.DoesNotExist:
        return HttpResponse('Ticket not found', status=404)

    if request.method == 'POST':
        comment_form = TicketCommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.ticket = ticket
            comment.user = request.user  # Assuming the user is logged in
            comment.save()
            return HttpResponseRedirect(f'/helpdesk/ticket/{ticket_id}/')  # Redirect to the same ticket detail page after saving
    else:
        comment_form = TicketCommentForm()

    return render(request, 'helpdesk/ticket_detail.html', {'ticket': ticket, 'comments': comments, 'comment_form': comment_form})

def edit_ticket(request, ticket_id):
    pass

def create_help_topic(request):
    """ Create a new help topic """
    if request.method == 'POST':
        form = HelpTopicForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse(f'Novo Tópico "{form.instance.name}" Adicionado com Sucesso')  # Redirect to success page after saving
    else:
        form = HelpTopicForm()
    return render(request, 'helpdesk/new_help_topic_form.html', {'form': form})