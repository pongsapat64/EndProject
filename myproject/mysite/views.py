from django.shortcuts import redirect, render
from mysite.models import Lecturer
from studentapp.forms import LoginForm, RegisterForm
from django.contrib.auth import (authenticate, 
                                 login, 
                                 logout)
from django.contrib import messages
from django.contrib.auth.models import User
# Create your views here.
def is_Lecturer(user):
    if isinstance(user, User):
        return user.roles.filter(name='Lecturer').exists()
    else:
        return False
    

def index(req):
    return render(req, 'index.html')


def login_view(req):
    if req.method == 'POST':
        form = LoginForm(req.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(req, username=username, password=password)
            if user is not None:
                login(req, user)
                messages.success(req, 'Login successful.')
                if is_Lecturer:
                    return redirect('main')
            return redirect('status')
        else:
            messages.error(req, 'Invalid username or password.')      
    else:
        form = LoginForm()

    return render(req, 'login.html', {'form': form})


def logout_view(req):
    logout(req)
    return redirect('login')


def register(req):
    if req.method == 'POST':
        form = RegisterForm(req.POST)
        if form.is_valid():
            user = form.save()
            login(req, user)
            return redirect('login')  
    else:
        form = RegisterForm()

    return render(req, 'register.html', {'form': form})
