from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import redirect, render
from mysite.models import Lecturer
from mysite.forms import LoginForm, RegisterForm, UserCreateForm, UserProfileForm
from django.contrib.auth import (authenticate, 
                                 login, 
                                 logout)
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
# Create your views here.
def is_Lecturer(user):
    if isinstance(user, User):
        return user.roles.filter(name='Lecturer').exists()
    else:
        return False

def is_Student(user):
    if isinstance(user, User):
        return user.roles.filter(name='Student').exists()
    else:
        return False
    
def is_admin(user):
    if isinstance(user, User):
        return user.roles.filter(name='Admin').exists()
    else:
        return False


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
                if is_admin(user):
                    return redirect('read')
                elif is_Lecturer(user):
                    return redirect('main')  
                elif is_Student(user):
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


def read_user(req):
    obj = User.objects.all()
    return render(req, 'read.html', {'user':obj})

def create_user(req):
    if req.method == 'POST':
        form = UserCreateForm(req.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            if not User.objects.filter(username=username).exists():
                form.save()
                return redirect('read')
            else:
                return HttpResponse("Username is already taken.")
    else:
        form = UserCreateForm()
    return render(req, 'create.html', {'form': form})

def update_user(request, id):
    user = User.objects.get(pk=id)
    if request.method == 'POST':
        form = UserCreateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('read')  
    else:
        form = UserCreateForm(instance=user)
    return render(request, 'update.html', {'user': user})

def delete_user(req, id):
    user = User.objects.get(pk=id)
    user.delete()
    return redirect('read') 
