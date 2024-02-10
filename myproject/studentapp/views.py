from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import (authenticate, 
                                 login, 
                                 logout)
from django.contrib.auth.models import User
from studentapp.models import Student
from mysite.views import *
import calendar
from datetime import datetime, timedelta
from studentapp.forms import LoginForm, RegisterForm, UserProfileForm
from django.contrib.auth.decorators import login_required, user_passes_test
from mysite.models import TimeSlot
# from .forms import UserCreate
# Create your views here.
    
def is_Student(user):
    if isinstance(user, User):
        return user.roles.filter(name='Student').exists()
    else:
        return False

@user_passes_test(is_Student)
@login_required(login_url='/mysite/login')
def select_committee(req):
    return redirect(req, 'select_committee.html')

@user_passes_test(is_Student)
@login_required(login_url='/mysite/login')
def appointment(req, year=None, month=None, day=None):
    if year is None or month is None:
        now = datetime.now()
        year, month = now.year, now.month

    cal = calendar.monthcalendar(year, month)

    prev_month = month - 1 if month > 1 else 12
    prev_year = year - 1 if month == 1 else year
    next_month = month + 1 if month < 12 else 1
    next_year = year + 1 if month == 12 else year

    return render(req, 'appointment.html', {'calendar': cal, 'year': year, 'month': month, 'day': day,
                                                'prev_year': prev_year, 'prev_month': prev_month,
                                                'next_year': next_year, 'next_month': next_month})

@user_passes_test(is_Student)
@login_required(login_url='/mysite/login')
def appointment_time_select(req, year, month, day):
    context = {
        'year': year,
        'month': month,
        'day': day
    }
    return render(req, 'app_time_select.html', context)

@user_passes_test(is_Student)
@login_required(login_url='/mysite/login')
def appointment_details(req, year, month, day, start_time, end_time):
    context = {
        'year': year,
        'month': month,
        'day': day,
        'start_time': start_time,
        'end_time': end_time,
    }
    return render(req, 'app_details.html', context)


@user_passes_test(is_Student)
@login_required(login_url='/mysite/login')
def status(req):
    return render(req, 'status.html')

@user_passes_test(is_Student)
@login_required(login_url='/mysite/login')
def score(req):
    return render(req, 'score.html')

@user_passes_test(is_Student)
@login_required(login_url='/mysite/login')
def editprofile(req):
    if req.method == 'POST':
        form = UserProfileForm(req.POST)
        if form.is_valid():
            if req.user.is_authenticated:
                existing_user = User.objects.filter(user=req.user).first()

                if existing_user:
                    user = User.objects.get(user=req.user)
                    form = UserProfileForm(req.POST, instance=user)
                    if form.is_valid():
                        form.instance.owner = req.user
                        form.save()
                        return render(req,'editprofile.html',{'user':user})
                else:
                    user = form.save(commit=False)
                    user.user = req.user
                    user.save()
                    return redirect('/')  
            else:
                return redirect('login')
        else:
            print(form.errors)
    else:
        form = UserProfileForm()
    return render(req, 'editprofile.html', {'form': form})