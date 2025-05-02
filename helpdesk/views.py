""" helpdesk/views.py """
import logging, json

from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse

from .models import Ticket, HelpTopic, TicketComment, TicketAttachment, Tasks, TaskComments
from .forms import TicketForm, HelpTopicForm, TicketCommentForm, TicketAttachmentForm, TasksForm, TaskCommentForm
from users.models import Agents

# Create your views here.
def index(request):
    """ Index page for helpdesk """
    # This is the landing page for the helpdesk application
    if request.user.is_authenticated:
        user_is_staff_member = Agents.objects.filter(user=request.user).values_list('privilege_level', flat=True)
        if user_is_staff_member.exists():
            # Check if the user is a staff member and redirect to the admin page:
            return redirect('admin_page')
    return render(request, 'helpdesk/index.html')

@login_required
def admin_page(request):
    """ Admin page for helpdesk """
    help_topics = HelpTopic.objects.all()
    tickets = Ticket.objects.all()
    return render(request, 'helpdesk/admin_page.html', {'help_topics': help_topics, 'tickets': tickets})

# Ticket views
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
@user_passes_test(lambda user: user.agent.privilege_level == 'admin')
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
@user_passes_test(lambda user: user.agent.privilege_level == 'admin')
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

# Fim de ticket views

# Task views
@login_required
def task_list(request):
    """ List all tasks """
    user_is_staff_member = Agents.objects.filter(user=request.user).values_list('privilege_level', flat=True)

    if not user_is_staff_member:
        return HttpResponse('Você não tem permissão para acessar essa página', status=403)

    if request.user.agent.privilege_level == 'admin':
        tasks = Tasks.objects.all()
    else:
        tasks = Tasks.objects.all().filter(assigned_to=request.user.agent)
    # You might want to add pagination or filtering here
    return render(request, 'helpdesk/task_list.html', {'tasks': tasks})

@login_required
@user_passes_test(lambda user: user.agent.privilege_level == 'admin')
def create_new_task(request):
    """ Create a new task """
    logger = logging.getLogger(__name__)
    
    if request.method == 'POST':
        form = TasksForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            agent = Agents.objects.get(user=request.user)
            task.created_by = agent
            logger.info(f'Task created: {task.task_name} by {request.user.username}')
            # Here you would typically send an email notification or perform other actions
            return HttpResponseRedirect(reverse(
                'task_detail',
                kwargs={'task_id': task.id}
            ))  # Redirect to task detail page after saving
    else:
        form = TasksForm()
    return render(request, 'helpdesk/new_task_form.html', {'form': form})

@login_required
def task_detail(request, task_id):
    """ View task details """
    user_is_staff_member = Agents.objects.filter(user=request.user).values_list('privilege_level', flat=True)
    if not user_is_staff_member:
        return HttpResponse('Você não tem permissão para acessar essa página', status=403)

    try:
        task = Tasks.objects.get(id=task_id)
        comments = TaskComments.objects.filter(task=task)
    except Tasks.DoesNotExist:
        return HttpResponse('Task not found', status=404)

    if request.method == 'POST':
        comment_form = TicketCommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.task = task
            comment.user = request.user  # Assuming the user is logged in
            comment.save()
            return HttpResponseRedirect(f'/task/{task_id}/')  # Redirect to the same task detail page after saving
    else:
        comment_form = TicketCommentForm()

    return render(request, 'helpdesk/task_detail.html', {'task': task, 'comments': comments, 'comment_form': comment_form})

@login_required
@user_passes_test(lambda user: user.agent.privilege_level == 'admin')
def delete_task(request, task_id):
    """ Delete a task """
    # This function would typically handle deleting a task
    # For now, we'll just return a dummy response
    task = Tasks.objects.get(id=task_id)
    if not task:
        return HttpResponse('Task not found', status=404)

    if request.method == 'POST':
        task = Tasks.objects.get(id=task_id)
        task.delete()
        return HttpResponseRedirect(reverse('task_list'))  # Redirect to task list page after deleting
    else:
        return render(request, 'helpdesk/delete_task_form.html', {'task': task})

@login_required
@user_passes_test(lambda user: user.agent.privilege_level == 'admin')
def edit_task(request, task_id):
    """ update task """
    logger = logging.getLogger(__name__)
    task = Tasks.objects.get(id=task_id)
    if request.method == 'POST':
        form = TasksForm(request.POST, instance=task)
        if form.is_valid():
            task_form = form.save(commit=False)
            agent = Agents.objects.get(user=request.user)
            task_form.created_by = agent
            task_form.save()
            # Log the task update
            logger.info(f'Task created: {task_form.task_name} by {request.user.username}')
            # Here you would typically send an email notification or perform other actions
            return HttpResponseRedirect(reverse(
                'task_detail',
                kwargs={'task_id': task_form.id}
            ))  # Redirect to task detail page after saving
    else:
        form = TasksForm(instance=task)  # Assuming the task exists
    return render(request, 'helpdesk/update_task_form.html', {'form': form, 'task': task})

@login_required
def create_task_comment(request, task_id):
    """ Create a new task comment """
    logger = logging.getLogger(__name__)

    user_is_staff_member = Agents.objects.filter(user=request.user).values_list('privilege_level', flat=True)
    if not user_is_staff_member:
        return HttpResponse('Você não tem permissão para acessar essa página', status=403)

    if request.method == 'POST':
        form = TaskCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.task = Tasks.objects.get(id=task_id)  # Assuming the task exists
            comment.user = request.user  # Assuming the user is logged in
            comment.save()
            logger.info(f'Task comment created: {comment.comment} by {request.user.username}')
            return HttpResponseRedirect(reverse(
                'task_detail',
                kwargs={'task_id': task_id}
            ))  # Redirect to task detail page after saving
    else:
        form = TaskCommentForm()
    return render(request, 'helpdesk/new_task_comment_form.html', {'form': form})

def assign_task(request, task_id):
    """ Assign a task to an agent """
    # This function would typically handle assigning a task to an agent
    # For now, we'll just return a dummy response
    if request.method == 'POST':
        try:
            agent_id = request.POST.get('agent_id')
            # Assuming you have a way to assign tasks to agents
            if agent_id == 'success':
                return JsonResponse({'status': 'success'})
            elif agent_id == 'error':
                return JsonResponse({'status': 'error', 'message': 'Error assigning task'}, status=400)
            
            agent = Agents.objects.get(id=agent_id)  # Assuming you have an Agent model

            task = Tasks.objects.get(id=task_id)
            task.assigned_to = agent  # Assuming 'assigned_to' is a field in your Task model
            task.save()
            
            # Log the assignment
            logger = logging.getLogger(__name__)
            logger.info(f'Task {task_id} assigned to agent {agent_id} by {request.user.username}')
            
            return HttpResponseRedirect(reverse(
                'task_detail',
                kwargs={'task_id': task.id}
            ))  # Redirect to task detail page after saving
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)
    else:
        # Assuming you have an Agent model and a way to get all agents
        return render(request, 'helpdesk/assign_task_form.html', {'agents': Agents.objects.all(), 'task_id': task_id})

def change_task_status(request, task_id):
    """ Change the status of a task """
    # This function would typically handle changing the status of a task
    # For now, we'll just return a dummy response
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            task_id = task_id
            new_status = data.get('status')

            # Validate the task ID and new status here
            if not task_id or not new_status:
                return JsonResponse({'status': 'error', 'message': 'Invalid task ID or status'}, status=400)

            task = Tasks.objects.get(id=task_id)
            task.status = new_status  # Assuming 'status' is a field in your Task model
            task.save()
            # Log the status change
            logger = logging.getLogger(__name__)
            logger.info(f'Task {task_id} status changed to {new_status} by {request.user.username}')
            
            return JsonResponse({'status': new_status})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)