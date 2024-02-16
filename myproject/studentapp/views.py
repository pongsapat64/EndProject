from django.shortcuts import redirect, render
from django.contrib.auth import (authenticate, login, logout)
from django.contrib.auth.models import User
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

def select_committee(req):
        if req.method == 'POST':
            form = SelectForm(req.POST)
            if form.is_valid():
                print(form)
                return redirect('appo')
        else:
            form = SelectForm()
        return render(req, 'select_com.html', {'form': form})

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
    if req.method == 'POST':
        form = SelectForm(req.POST)
        if form.is_valid():
            selected_ids = form.cleaned_data['items'] 
            selected_options = [item.id for item in selected_ids] 
            req.session['selected_options'] = selected_options

    else:
        form = SelectForm()

    context = {
        'year': year,
        'month': month,
        'day': day,
        'start_time': start_time,
        'end_time': end_time,
        'form' : form
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


def create_event_with_attendees(start_time_str, end_time_str, summary, attendees, description=None,Schedule_id=None, location=None):
    service = get_calendar_service()

    event = {
        "summary": summary,
        "description": description,
        "location": location,
        "start": {"dateTime": start_time_str, "timeZone": 'Asia/Bangkok'},
        "end": {"dateTime": end_time_str, "timeZone": 'Asia/Bangkok'},
        "attendees": [{"email": attendee} for attendee in attendees],
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
                './client_secret_776983342224-8ab8a7lsg5n1a2t5ofdghmt2qi2n10g8.apps.googleusercontent.json', SCOPES)
            creds = flow.run_local_server(port=40001)
        with open('token.pkl', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    return service



def create_event_with_attendees2(req):
    start_time = Lecturer
    end_time = "2024-02-16T12:00:00"
    summary = "Meeting with Team"
    attendees = ["pongsapat.ch.64@ubu.ac.th"]
    description = "Discussion about project progress"
    location = "Conference Room A"
    create_event_with_attendees(start_time, end_time, summary, attendees, description, location)
    return redirect('status')

