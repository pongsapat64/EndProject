from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from google.oauth2 import id_token
from django.conf import settings
from google.auth.transport import requests
from google.auth.transport.requests import Request
import pickle
import os.path
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from django.contrib.auth.hashers import make_password
from mysite.models import *
from mysite.forms import *
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
                    return redirect('profileLec')  
                elif is_Student(user):
                    return redirect('profile') 
            else:
                messages.error(req, 'ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง!.')
        else:
            messages.error(req, 'กรุณากรอกข้อมูลในทุกช่องที่จำเป็น!')
    else:
        form = LoginForm()

    return render(req, 'login.html', {'form': form})



def logout_view(req):
    logout(req)
    return redirect('/')


def register(req):
    if req.method == 'POST':
        form = RegisterForm(req.POST)
        if form.is_valid():
            user = form.save(commit=False)  # บันทึกข้อมูลลงไปในฟอร์มก่อน
            user.backend = 'django.contrib.auth.backends.ModelBackend'  # ระบุการตรวจสอบสิทธิ์แบ็กเอนด์
            user.save()  # บันทึกผู้ใช้ใหม่ลงฐานข้อมูล
            login(req, user)
            return redirect('login')
        else:
            messages.error(req, 'กรุณากรอกข้อมูลในทุกช่องที่จำเป็น!')
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
            password = form.cleaned_data['password']
            if not User.objects.filter(username=username).exists():
                # สร้างผู้ใช้ใหม่
                user = form.save(commit=False)
                # กำหนดรหัสผ่านให้กับผู้ใช้และเข้ารหัสรหัสผ่าน
                user.password = make_password(password)
                user.save()
                return redirect('read')
            else:
                return HttpResponse("ชื่อผู้ใช้ถูกใช้แล้ว.")
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

@user_passes_test(is_Student)
@login_required(login_url='/mysite/login')
def show_committee(req):
    lecturers = Lecturer.objects.all()
    advisers = Adviser.objects.all()
    return render(req, 'show_committee.html', {'lecturers': lecturers, 'adviser':advisers})
    

@user_passes_test(is_Student)
@login_required(login_url='/mysite/login')
def appointment(req):
    return render(req, 'appointment.html')


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

@user_passes_test(is_Lecturer)
@login_required(login_url='/mysite/login')
def mainpage(req):
    lecturers = Lecturer.objects.get(user=req.user)
    lecturer = Appointment.objects.filter(committee=lecturers)
    return render(req, "mainpage.html", {'appointments': lecturer})


@user_passes_test(is_Lecturer)
@login_required(login_url='/mysite/login')
def addtime(req,):
    return render(req, 'addtime.html')


def get_freetime(req):
    freetimes = AvailableTime.objects.all()
    events = []

    for freetime in freetimes:
        event = {
            'id': freetime.id,
            'title': f'{freetime.lecturer.first_name}  {freetime.lecturer.last_name}',
            'start': freetime.date.strftime('%Y-%m-%d') + 'T' + freetime.start_time.strftime('%H:%M:%S'),
            'end': freetime.date.strftime('%Y-%m-%d') + 'T' + freetime.end_time.strftime('%H:%M:%S'),
            'backgroundColor': '#3b3b3b'  
        }
        events.append(event)

    return JsonResponse(events, safe=False)

@user_passes_test(is_Lecturer)
@login_required(login_url='/mysite/login')
def create_freetime(req):
    if req.method == 'POST':
        lecturer = req.user.lecturer  # สมมติว่ามีการสร้าง field lecturer ในโมเดล Lecturer

        if lecturer:  # ตรวจสอบว่าผู้ใช้ปัจจุบันเป็นอาจารย์หรือไม่
            start_time = req.POST.get('start_time')
            end_time = req.POST.get('end_time')
            date = req.POST.get('date')

            # ตรวจสอบว่ามีข้อมูลเวลาที่มี lecturer_id และ start_time และ end_time และ date เดียวกันหรือไม่
            if not AvailableTime.objects.filter(lecturer_id=lecturer.id, start_time=start_time, end_time=end_time, date=date).exists():
                # สร้างหรืออัพเดทวันเวลาที่ใช้งานได้
                available_time = AvailableTime.objects.create(
                    lecturer=lecturer,
                    start_time=start_time,
                    end_time=end_time,
                    date=date
                )
                return redirect('addtime')
            else:
                return JsonResponse({'status': 'error', 'message': 'ข้อมูลซ้ำกัน'})
        else:
            return JsonResponse({'status': 'error', 'message': 'คุณไม่ใช่อาจารย์'})
    else:
        return render(req, 'addthetime.html')

@user_passes_test(is_Lecturer)
@login_required(login_url='/mysite/login')    
def showAvailableTime(req):
    avt = AvailableTime.objects.all()
    return render(req, 'showavt.html', {'show':avt})


@user_passes_test(is_Lecturer)
@login_required(login_url='/mysite/login')
def deleteAvailableTime(req, id):
    avt = AvailableTime.objects.get(pk=id)
    avt.delete()
    return redirect('showavt') 


@user_passes_test(is_Lecturer)
@login_required(login_url='/mysite/login')
def addtime_select(request, year=None, month=None, day=None):
    context = {
        'year': year,
        'month': month,
        'day': day
    }
    return render(request, 'addtimeselect.html', context)

@user_passes_test(is_Lecturer)
@login_required(login_url='/mysite/login')
def history(req):
    appointments = Appointment.objects.all()
    return render(req, 'history.html', {'appointments': appointments})


@user_passes_test(is_Lecturer)
@login_required(login_url='/mysite/login')
def profileLec(req):
    if req.method == 'POST':
        user = req.user
        user.lecturer.first_name = req.POST.get('first_name')
        user.lecturer.last_name = req.POST.get('last_name')
        user.lecturer.email = req.POST.get('email')
        
        user.save()
        user.lecturer.save()
        
        return redirect('profileLec')
        
    return render(req, 'profileLec.html')

user_passes_test(is_Lecturer)
@login_required(login_url='/mysite/login')
def give_score(req, id):
    student = Student.objects.get(pk=id)
    lecturer = Lecturer.objects.get(user=req.user)
    if req.method == 'POST':
        obj = Score.objects.create(student=student, lecturer=lecturer, scored=req.POST['scored'])
        obj.save()
        return redirect('showstudents')

    return render(req, 'givescore.html')

user_passes_test(is_Lecturer)
@login_required(login_url='/mysite/login')
def show_student(req):
    student = Student.objects.all()
    return render(req, 'showstudents.html', {'student':student})