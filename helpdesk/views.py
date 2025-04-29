""" helpdesk/views.py """
import logging, json

from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse

from .models import Ticket, HelpTopic, TicketComment #, TicketAttachment
from .forms import TicketForm, HelpTopicForm, TicketCommentForm #, TicketAttachmentForm
from users.models import Agents

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
    user_is_staff_member = Agents.objects.filter(user=request.user).values_list('privilege_level', flat=True)
    # admin pode ver todos os tickets, enquanto os outros usuários podem ver apenas os tickets atribuídos a eles
    if user_is_staff_member[0] == 'admin':
        tickets = Ticket.objects.all()
    else:
        tickets = Ticket.objects.filter(assigned_to=request.user.agent)  # Assuming the user is logged in and has a related Ticket object
    # You might want to add pagination or filtering here
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
            return HttpResponseRedirect(reverse(
                'ticket_detail',
                kwargs={'ticket_id': ticket.id}
            ))  # Redirect to ticket detail page after saving
    else:
        form = TicketForm()
    return render(request, 'helpdesk/new_ticket_form.html', {'form': form})

@login_required
def check_ticket(request):
    """ Check the status of a ticket """
    title = 'check_ticket'
    
    if request.method == 'POST':
        user = request.user  # Assuming the user is logged in
        try:
            ticket_id = request.POST.get('ticket_id')
            ticket = Ticket.objects.get(id=ticket_id, user=user)  # Ensure the ticket belongs to the user
            return HttpResponseRedirect(reverse(
                'ticket_detail',
                kwargs={'ticket_id': ticket.id}
            ))  # Assuming 'status' is a field in your Ticket model
        except Ticket.DoesNotExist:
            # Handle the case where the ticket does not exist or does not belong to the user
            # You might want to log this or show a message to the user
            logger = logging.getLogger(__name__)
            logger.warning(f'Ticket {ticket_id} not found or does not belong to user {user.username}')
            # Here you could render a template with an error message or redirect to an error page
            return HttpResponse('O Ticket não foi encontrado ou não pertence a esse usuário', status=404)
        # For now, we'll just redirect to a dummy ticket detail page
    return render(request, 'helpdesk/check_ticket_form.html', {'title': title})

@login_required
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
            return HttpResponseRedirect(f'/ticket/{ticket_id}/')  # Redirect to the same ticket detail page after saving
    else:
        comment_form = TicketCommentForm()

    return render(request, 'helpdesk/ticket_detail.html', {'ticket': ticket, 'comments': comments, 'comment_form': comment_form})

@login_required
def change_ticket_status(request):
    """ Change the status of a ticket """
    # This function would typically handle changing the status of a ticket
    # For now, we'll just return a dummy response
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            ticket_id = data.get('ticket_id')
            new_status = data.get('status')

            # Validate the ticket ID and new status here
            if not ticket_id or not new_status:
                return JsonResponse({'status': 'error', 'message': 'Invalid ticket ID or status'}, status=400)

            ticket = Ticket.objects.get(id=ticket_id)
            ticket.status = new_status  # Assuming 'status' is a field in your Ticket model
            ticket.save()
            # Log the status change
            logger = logging.getLogger(__name__)
            logger.info(f'Ticket {ticket_id} status changed to {new_status} by {request.user.username}')
            
            return JsonResponse({'status': new_status})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

@login_required
@user_passes_test(lambda u: u.is_superuser or u.agent.privilege_level == 'admin')
def assign_ticket(request, ticket_id):
    """ Assign a ticket to an agent """
    # This function would typically handle assigning a ticket to an agent
    # For now, we'll just return a dummy response
    if request.method == 'POST':
        try:
            agent_id = request.POST.get('agent_id')
            # Assuming you have a way to assign tickets to agents
            if agent_id == 'success':
                return JsonResponse({'status': 'success'})
            elif agent_id == 'error':
                return JsonResponse({'status': 'error', 'message': 'Error assigning ticket'}, status=400)
            
            agent = Agents.objects.get(id=agent_id)  # Assuming you have an Agent model

            ticket = Ticket.objects.get(id=ticket_id)
            ticket.assigned_to = agent  # Assuming 'assigned_to' is a field in your Ticket model
            ticket.save()
            
            # Log the assignment
            logger = logging.getLogger(__name__)
            logger.info(f'Ticket {ticket_id} assigned to agent {agent_id} by {request.user.username}')
            
            return HttpResponseRedirect(reverse(
                'ticket_detail',
                kwargs={'ticket_id': ticket.id}
            ))  # Redirect to ticket detail page after saving
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)
    else:
        # Assuming you have an Agent model and a way to get all agents
        return render(request, 'helpdesk/assign_ticket_form.html', {'agents': Agents.objects.all(), 'ticket_id': ticket_id})

@login_required
def edit_ticket(request, ticket_id):
    pass

@login_required
def delete_ticket(request, ticket_id):
    pass

@login_required
@user_passes_test(lambda u: u.agent.privilege_level == 'admin')
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