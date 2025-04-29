""" User views for the application. """
from django.shortcuts import redirect, render, HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test

from .forms import UserRegistrationForm, AgentRegistrationForm
from .models import Agents

def user_registration(request):
    """
    View for user registration.
    """
    # redireciona para a página home se o usuário já estiver activo no site e não for um agente com nível de privilégio 'admin'
    try:
        if request.user.is_authenticated and request.user.agent.privilege_level != 'admin':
            return redirect('admin_page')
    except Agents.DoesNotExist:
        return HttpResponse("Algo aconteceu, não conseguimos encontrar a página.", status=404)

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # Aqui você pode adicionar lógica para enviar um e-mail de confirmação, se necessário
            user.save()
            return redirect('success')
        # Se o formulário não for válido, renderiza novamente a página com os erros do formulário
        return render(request, 'users/user_registration_form.html', {'form': form})
    form = UserRegistrationForm()
    return render(request, 'users/user_registration_form.html', {'form': form})

def success(request):
    """
    View for success page after registration.
    """
    # redireciona para a página home se o usuário já estiver activo no site e não for um superuser ou não for um agente com nível de privilégio 'admin'
    try:
        if request.user.is_authenticated and request.user.agent.privilege_level == 'admin':
            return redirect('admin_page')
        else:
            return redirect('login')
    except Agents.DoesNotExist:
        return HttpResponse("Algo aconteceu, não conseguimos encontrar a página.", status=404)

def user_login(request):
    """
    View for user login.
    """
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            user_is_staff_member = Agents.objects.filter(user=user).values_list('privilege_level', flat=True)
            # Se o usuário for um usuário com nível de privilégio 'admin', 'suporte', 'agente' redireciona para a página de administração
            # se não, redireciona para a página inicial
            if user_is_staff_member:
                return redirect('admin_page')
            else:
                return redirect('index')
        else:
            return HttpResponse("Invalid login credentials")
    return render(request, 'users/login.html')

@login_required
@user_passes_test(lambda u: u.agent.privilege_level == 'admin')
def agent_registration(request):
    """
    View for agent registration.
    """
    if request.method == 'POST':
        form = AgentRegistrationForm(request.POST)
        if form.is_valid():
            agent = form.save()
            agent.save()
            return HttpResponseRedirect(reverse(
                'agent_detail',
                kwargs={'pk': agent.pk}))
        # Se o formulário não for válido, renderiza novamente a página com os erros do formulário
        return render(request, 'users/agent_registration_form.html', {'form': form})
    form = AgentRegistrationForm()
    return render(request, 'users/agent_registration_form.html', {'form': AgentRegistrationForm})


@login_required
@user_passes_test(lambda u: u.agent.privilege_level == 'admin')
def agent_detail(request, pk):
    """
    View for agent detail.
    """
    agent = Agents.objects.get(pk=pk)
    tickets = agent.assigned_tickets.all()  # Assuming you have a related name for the tickets assigned to the agent
    return render(request, 'users/agent_detail.html', {'agent': agent, 'tickets': tickets})

@login_required
@user_passes_test(lambda u: u.agent.privilege_level == 'admin')
def agent_update(request, pk):
    """
    View for agent update.
    """
    agent = Agents.objects.get(pk=pk)
    if request.method == 'POST':
        form = AgentRegistrationForm(request.POST, instance=agent)
        if form.is_valid():
            agent = form.save()
            agent.save()
            return HttpResponseRedirect('agent_detail', args=[agent.pk])
        # Se o formulário não for válido, renderiza novamente a página com os erros do formulário
        return render(request, 'users/agent_update_form.html', {'form': form})
    form = AgentRegistrationForm(instance=agent)
    return render(request, 'users/agent_update_form.html', {'form': form, 'agent': agent})

@login_required
def agent_list(request):
    """
    View for agent list.
    """
    # redireciona para a página home se o usuário não for um superuser ou não for um agente com nível de privilégio 'admin'
    # Se o usuário não for um superuser ou não for um agente com nível de privilégio 'admin', levantamos um erro http500
    try:
        user_is_staff_member = Agents.objects.filter(user=request.user).values_list('privilege_level', flat=True)
        if not user_is_staff_member:
            return HttpResponse("Infelizmente você não tem autorização para aceder a essa página.")
    except Agents.DoesNotExist:
        return HttpResponse("Infelizmente você não tem autorização para aceder a essa página.") 

    agents = Agents.objects.all()
    return render(request, 'users/agent_list.html', {'agents': agents})