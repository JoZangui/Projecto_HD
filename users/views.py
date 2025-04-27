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
    # redireciona para a página home se o usuário já estiver activo no site
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.save()
            # Criar um processo de confirmação de e-mail
            login(request, user)
            return HttpResponseRedirect('success')
        return render(request, 'users/user_registration_form.html', {'form': form})
    form = UserRegistrationForm()
    return render(request, 'users/user_registration_form.html', {'form': form})

def success(request):
    return render(request, 'users/success.html')


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
            if user.is_superuser:
                return redirect('admin_page')
            elif user.is_staff:
                return redirect('admin_page')
            else:
                return redirect('index')
        else:
            return HttpResponse("Invalid login credentials")
    return render(request, 'users/login.html')

@login_required
def agent_registration(request):
    """
    View for agent registration.
    """
    # redireciona para a página home se o usuário não for um superuser ou não for um agente com nível de privilégio 'admin'
    # Se o usuário não for um superuser ou não for um agente com nível de privilégio 'admin', levantamos um erro http500
    try:
        if not request.user.is_superuser and request.user.agent.privilege_level != 'admin':
            return HttpResponse("Infelizmente você não tem autorização para aceder a essa página.")
    except Agents.DoesNotExist:
        return HttpResponse("Infelizmente você não tem autorização para aceder a essa página.") 

    if request.method == 'POST':
        form = AgentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.save()
            # Criar um processo de confirmação de e-mail
            login(request, user)
            return HttpResponseRedirect('success')
        return render(request, 'users/agent_registration_form.html', {'form': form})
    form = AgentRegistrationForm()
    return render(request, 'users/agent_registration_form.html', {'form': AgentRegistrationForm})
