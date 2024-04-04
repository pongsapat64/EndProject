from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth import (authenticate, login, logout)
from django.contrib.auth.models import User
from mysite.models import Score
from mysite.views import *
import calendar
from datetime import datetime
from mysite.forms import *
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import pickle
import os.path

from social_core.backends.google import GoogleOAuth2
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.decorators import login_required, user_passes_test
# Create your views here.
    
def is_Student(user):
    if isinstance(user, User):
        return user.roles.filter(name='Student').exists()
    else:
        return False

def show_committee(req):
    lecturers = Lecturer.objects.all()
    return render(req, 'show_committee.html', {'lecturers': lecturers})
    

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
                                            'next_year': next_year, 'next_month': next_month,})

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
    student = Student.objects.get(user=req.user)
    context = {
        'year': year,
        'month': month,
        'day': day,
        'start_time': start_time,
        'end_time': end_time,
        'student': student,
    }
    return render(req, 'app_details.html', context)
    

@user_passes_test(is_Student)
@login_required(login_url='/mysite/login')
def status(req):
    return render(req, 'status.html')

@user_passes_test(is_Student)
@login_required(login_url='/mysite/login')
def score(req):
    student = Student.objects.get(user=req.user)
    score = Score.objects.filter(student=student)
    context = {
        'student': student,
        'score': score,
    }
    return render(req, 'score.html', context)

@user_passes_test(is_Student)
@login_required(login_url='/mysite/login')
def editprofile(req):
    user_form = UserProfileForm(instance=req.user)
    student_form = StudentProfileForm(instance=req.user.student)

    if req.method == 'POST':
        user_form = UserProfileForm(req.POST, instance=req.user)
        student_form = StudentProfileForm(req.POST, instance=req.user.student)
        if user_form.is_valid() and student_form.is_valid():
            user_form.save()
            student_form.save()
            return redirect('edit')
    
    return render(req, 'editprofile.html', {'user_form': user_form, 'student_form': student_form})


def create_google_calendar_event(start_time_str, end_time_str, summary, Lecturer):
    service = get_calendar_service()

    event = {
        "summary": summary,
        "start": {"dateTime": start_time_str, "timeZone": 'Asia/Bangkok'},
        "end": {"dateTime": end_time_str, "timeZone": 'Asia/Bangkok'},
        "email": [{"email": email } for email in Lecturer],
    }
    event_result = service.events().insert(calendarId='primary', body=event, sendNotifications=True).execute()

SCOPES = ['https://www.googleapis.com/auth/calendar']
def get_calendar_service():
    creds = None
    if os.path.exists('token.pkl'):
        with open('token.pkl', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                './client_secret_776983342224-8ab8a7lsg5n1a2t5ofdghmt2qi2n10g8.apps.googleusercontent.com.json', SCOPES)
            creds = flow.run_local_server(port=40001)
        with open('token.pkl', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    return service


def create_google_calendar_event2(request):
    # Assuming checkboxes are named 'lecturers' and each checkbox value contains lecturer ids
    lecturer_ids_selected = request.POST.getlist('lecturers')
    
    # Retrieve the email addresses of selected lecturers
    emails = Lecturer.objects.filter(id__in=lecturer_ids_selected).values_list('user__email', flat=True)
    
    # Assuming create_google_calendar_event is a function to create a Google Calendar event
    # You should replace this with your actual function to create the event
    start_time = "2024-04-16T10:00:00"
    end_time = "2024-04-16T12:00:00"
    summary = "Meeting with Team"
    create_google_calendar_event(start_time, end_time, summary, emails)
    
    return redirect('status')

