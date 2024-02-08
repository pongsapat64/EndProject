from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import (authenticate, 
                                 login, 
                                 logout)
from django.contrib.auth.models import User
from mysite.views import *
import calendar
from datetime import datetime, timedelta
from studentapp.forms import ExtendedStudentProfileForm, LoginForm, RegisterForm, UserProfileForm
from django.contrib.auth.decorators import login_required
from mysite.models import TimeSlot
# from .forms import UserCreate
# Create your views here.

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful.')
                return redirect('status') 
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')  
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})

@login_required(login_url='/studentapp/login')
def select_committee(request):
    return redirect(request, 'select_committee.html')

@login_required(login_url='/studentapp/login')
def appointment(request, year=None, month=None, day=None):
    if year is None or month is None:
        now = datetime.now()
        year, month = now.year, now.month

    cal = calendar.monthcalendar(year, month)

    prev_month = month - 1 if month > 1 else 12
    prev_year = year - 1 if month == 1 else year
    next_month = month + 1 if month < 12 else 1
    next_year = year + 1 if month == 12 else year

    return render(request, 'appointment.html', {'calendar': cal, 'year': year, 'month': month, 'day': day,
                                                'prev_year': prev_year, 'prev_month': prev_month,
                                                'next_year': next_year, 'next_month': next_month})

@login_required(login_url='/studentapp/login')
def appointment_time_select(request, year, month, day):
    context = {
        'year': year,
        'month': month,
        'day': day
    }
    return render(request, 'app_time_select.html', context)


@login_required(login_url='/studentapp/login')
def appointment_details(request, year, month, day, start_time, end_time):
    context = {
        'year': year,
        'month': month,
        'day': day,
        'start_time': start_time,
        'end_time': end_time,
    }
    return render(request, 'app_details.html', context)



@login_required(login_url='/studentapp/login')
def status(request):
    return render(request, 'status.html')

@login_required(login_url='/studentapp/login')
def score(request):
    return render(request, 'score.html')

@login_required(login_url='/studentapp/login')
def editprofile(request):
    user = request.user

    # สร้างฟอร์ม UserProfileForm และ ExtendedStudentForm
    form = UserProfileForm(instance=user)
    extended_form = ExtendedStudentProfileForm(instance=user.student) if hasattr(user, 'student') else ExtendedStudentProfileForm()

    if request.method == 'POST':
        user = request.user
        # ในกรณีที่มีการส่งข้อมูลแบบ POST
        form = UserProfileForm(request.POST, instance=user)
        extended_form = ExtendedStudentProfileForm(request.POST, instance=user.student) if hasattr(user, 'student') else ExtendedStudentProfileForm(request.POST)

        if form.is_valid() and extended_form.is_valid():
            form.save()
            # บันทึกข้อมูลของ ExtendedStudentForm และผูกกับ user ปัจจุบัน
            extended_instance = extended_form.save(commit=False)
            extended_instance.user = user
            extended_instance.save()

            return redirect('editprofile')  # หรือไปยังหน้าที่คุณต้องการหลังจากการแก้ไขโปรไฟล์

    context = {
        "user": user,
        "form": form,
        "extended_form": extended_form
    }
    return render(request, 'editprofile.html', context)
