from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import (authenticate, login, logout)
from django.contrib.auth.models import User
from studentapp.models import Project
from mysite.models import Appointment, Score
from mysite.views import *
import calendar
from django.core.serializers.json import DjangoJSONEncoder
import json
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
    advisers = Adviser.objects.all()
    return render(req, 'show_committee.html', {'lecturers': lecturers, 'adviser':advisers})
    

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
    student = Student.objects.get(user=req.user)
    appointments = Appointment.objects.filter(student=student)
    return render(req, 'status.html', {'appointments': appointments})

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
def profile(req):
    if req.method == 'POST':
        user = req.user
        user.first_name = req.POST.get('first_name')
        user.last_name = req.POST.get('last_name')
        user.email = req.POST.get('email')
        user.student.student_id = req.POST.get('student_id')
        user.student.subject = req.POST.get('subject')
        
        user.save()
        user.student.save()
        
        return redirect('profile')
        
    return render(req, 'profile.html')



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


def create_google_calendar_event(start_time_str, end_time_str, summary, lecturers_emails, description=None, location=None):
    service = get_calendar_service()

    event = {
        "summary": summary,
        "start": {"dateTime": start_time_str, "timeZone": 'Asia/Bangkok'},
        "end": {"dateTime": end_time_str, "timeZone": 'Asia/Bangkok'},
        "attendees": [{"email": email} for email in lecturers_emails],
    }
    event_result = service.events().insert(calendarId='primary', body=event, sendNotifications=True).execute()



@user_passes_test(is_Student)
@login_required(login_url='/mysite/login')
def create_google_calendar_event2(request):
    if request.method == 'POST':
        start_time_str = request.POST.get('start_time')
        start_time = start_time_str + ":00"
        end_time_str = request.POST.get('end_time')
        end_time = end_time_str + ":00"
        summary = request.POST.get('summary')
        
        lecturer_ids_selected = request.POST.getlist('lecturers')
        
        # Get emails of selected lecturers
        emails = Lecturer.objects.filter(id__in=lecturer_ids_selected).values_list('user__email', flat=True)

        # Add current user's email as organizer
        current_user_email = request.user.email

        # Send invitation to selected lecturers
        for email in emails:
            create_google_calendar_event(start_time, end_time, summary, [email, current_user_email])

        # Create Appointment instance
        student_instance = get_or_create_student_instance(request.user)
        committee_user = Lecturer.objects.get(id=lecturer_ids_selected[0])

        appointment = Appointment.objects.create(
            start_time=start_time_str,
            end_time=end_time_str,
            summary=summary,
            student=student_instance,
            committee=committee_user
        )
        appointment.save()
    
    return redirect('status')


def get_or_create_student_instance(user):
    # Check if a Student instance already exists for the given user
    try:
        student_instance = Student.objects.get(user=user)
    except Student.DoesNotExist:
        # If no Student instance exists, create one
        student_instance = Student.objects.create(user=user)
    
    return student_instance

@user_passes_test(is_Student)
@login_required(login_url='/mysite/login')
def create_project(request):
    if request.method == 'POST':
        topic = request.POST.get('topic')
        document = request.POST.get('document')
        presentationSlide = request.POST.get('presentationSlide')
        year = request.POST.get('year')
        
        # Save project to the database
        Project.objects.create(
            user=request.user,
            topic=topic,
            document=document,
            presentationSlide=presentationSlide,
            year=year
        )
        
        # Redirect to the project detail page
        return redirect('status')
    
    return render(request, 'create_project.html')

@user_passes_test(is_Student)
@login_required(login_url='/mysite/login')
def project_detail(req):
    projects = Project.objects.filter(user=req.user)
    return render(req, 'project_detail.html', {'projects': projects})