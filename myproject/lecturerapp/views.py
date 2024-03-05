from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from studentapp.models import Project
from mysite.models import AvailableTime, Score
from mysite.forms import *
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
import calendar
from datetime import datetime

# Create your views here.
def is_Lecturer(user):
    if isinstance(user, User):
        return user.roles.filter(name='Lecturer').exists()
    else:
        return False

@user_passes_test(is_Lecturer)
@login_required(login_url='/mysite/login')
def mainpage(req):
    return render(req, "mainpage.html")


@user_passes_test(is_Lecturer)
@login_required(login_url='/mysite/login')
def addtime(req, year=None, month=None, day=None):
    if year is None or month is None:
        now = datetime.now()
        year, month = now.year, now.month

    cal = calendar.monthcalendar(year, month)

    prev_month = month - 1 if month > 1 else 12
    prev_year = year - 1 if month == 1 else year
    next_month = month + 1 if month < 12 else 1
    next_year = year + 1 if month == 12 else year

    return render(req, 'addtime.html', {'calendar': cal, 'year': year, 'month': month, 'day': day,
                                            'prev_year': prev_year, 'prev_month': prev_month,
                                            'next_year': next_year, 'next_month': next_month})

def get_freetime(self, request, *args, **kwargs):
    events = []
    pets = AvailableTime.objects.all()

    for pet in pets:
        events.append({
            'start': pet.time.isoformat(),
            'end':pet.time.isoformat(),
            'date':pet.date.isoformat(),
        })

    return JsonResponse(events, safe=False)

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
    return render(req, "history.html")


@user_passes_test(is_Lecturer)
@login_required(login_url='/mysite/login')
def editprofile(req):
    user_form = UserProfileForm(instance=req.user)
    lecturer_form = LecturerProfileForm(instance=req.user.lecturer)

    if req.method == 'POST':
        user_form = UserProfileForm(req.POST, instance=req.user)
        lecturer_form = LecturerProfileForm(req.POST, instance=req.user.lecturer)
        if user_form.is_valid() and lecturer_form.is_valid():
            user_form.save()
            lecturer_form.save()
            return redirect('editlec')
    
    return render(req, 'editprofileLec.html', {'user_form': user_form, 'lecturer_form': lecturer_form})

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

    