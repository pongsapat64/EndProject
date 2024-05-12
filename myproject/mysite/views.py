from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from google.oauth2 import id_token
from django.conf import settings
from google.auth.transport import requests
from studentapp.models import Project, Student
from mysite.models import Adviser, Appointment, Lecturer
from mysite.forms import LoginForm, RegisterForm, UserCreateForm, UserProfileForm
from django.contrib.auth import (authenticate, 
                                 login, 
                                 logout)
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from allauth.account.auth_backends import AuthenticationBackend
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

def google_login(req):
    # Redirect the user to Google's authentication page
    # Implement your Google OAuth URL here
    google_auth_url = 'https://accounts.google.com/o/oauth2/auth?response_type=code&client_id=776983342224-8ab8a7lsg5n1a2t5ofdghmt2qi2n10g8.apps.googleusercontent.com&redirect_uri=http://127.0.0.1:8000/google/callback&scope=email%20profile&access_type=offline'
    return redirect(google_auth_url)


def google_callback(req):
    # Handle the callback from Google after authentication
    # Check if the error is "AuthAlreadyAssociated"
    error = req.GET.get('error')
    if error == 'AuthAlreadyAssociated':
        # Redirect to the regular login page with an error message
        return redirect('/login/?error=google_already_associated')


def logout_view(req):
    logout(req)
    return redirect('/')


def register(req):
    if req.method == 'POST':
        form = RegisterForm(req.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Don't save to the database yet
            user.backend = 'django.contrib.auth.backends.ModelBackend'  # Specify authentication backend
            user.save()  # Now save the user to the database
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

def create_adviser(req):
    if req.method == 'POST':
        lecturer_id = req.POST.get('lecturer')
        student_id = req.POST.get('student')
        lecturer = Lecturer.objects.get(id=lecturer_id)
        student = Student.objects.get(id=student_id)
        adviser = Adviser.objects.create(lecturer=lecturer, student=student)
        return redirect('read')
    else:
        lecturers = Lecturer.objects.all()
        students = Student.objects.all()
        return render(req, 'create_adviser.html', {'lecturers': lecturers, 'students': students})
    

def show_appoinment(req):
    appointment = Appointment.objects.all()
    return render(req, 'show_appoinment.html', {'appointment':appointment})


def add_adviser_to_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    if request.method == 'POST':
        adviser_id = request.POST.get('adviser')
        adviser = get_object_or_404(Adviser, pk=adviser_id)
        appointment.adviser = adviser
        appointment.save()
        return redirect('show_appoinment')
    
    advisers = Adviser.objects.all()
    return render(request, 'add_adviser_to_appointment.html', {'appointment': appointment, 'advisers': advisers})