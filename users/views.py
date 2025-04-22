""" User views for the application. """
from django.shortcuts import redirect, render, HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required

from .forms import UserRegistrationForm

def user_registration(request):
    """
    View for user registration.
    """
    # redireciona para a página home se o usuário já estiver activo no site
    if request.user.is_active:
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


def login(request):
    """
    View for user login.
    """
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return HttpResponse("Invalid login credentials")
    return render(request, 'users/login.html')