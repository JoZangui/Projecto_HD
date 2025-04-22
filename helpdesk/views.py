from django.shortcuts import render
from .forms import TicketForm, HelpTopicForm, TicketCommentForm #, TicketAttachmentForm
from django.http import HttpResponseRedirect

# Create your views here.
def index(request):
    return render(request, 'helpdesk/index.html')

def create_new_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user  # Assuming the user is logged in
            ticket.save()
            return HttpResponseRedirect('/helpdesk/ticket/status/')  # Redirect to ticket status page after saving
    else:
        form = TicketForm()
    return render(request, 'helpdesk/new_ticket_form.html', {'form': form})

def check_ticket_status(request):
    return render(request, 'helpdesk/check_ticket_status_form.html')

def ticket_detail(request, ticket_id):
    pass

def edit_ticket(request, ticket_id):
    pass