from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from studentapp.models import Project
from mysite.models import Appointment, AvailableTime, Score
from mysite.forms import *
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
import calendar
from datetime import datetime, timedelta

# Create your views here.
def is_Lecturer(user):
    if isinstance(user, User):
        return user.roles.filter(name='Lecturer').exists()
    else:
        return False

@user_passes_test(is_Lecturer)
@login_required(login_url='/mysite/login')
def mainpage(req):
    lecturers = Lecturer.objects.get(user=req.user)
    lecturer = Appointment.objects.filter(committee=lecturers)
    return render(req, "mainpage.html", {'appointments': lecturer})

    students = Student.objects.get(user=req.user)
    student = Appointment.objects.filter(student=students)
    return render(req, 'status.html', {'appointments': student})


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
            'title': f'{freetime.lecturer.first_name}  {freetime.lecturer.last_name}',   # ชื่อผู้สอนหรือข้อมูลอื่น ๆ ที่ต้องการแสดง
            'start': freetime.date.strftime('%Y-%m-%d') + 'T' + freetime.start_time.strftime('%H:%M:%S'),
            'end': freetime.date.strftime('%Y-%m-%d') + 'T' + freetime.end_time.strftime('%H:%M:%S'),
            'backgroundColor': '#3b3b3b'  # สีพื้นหลังของเหตุการณ์
        }
        events.append(event)

    return JsonResponse(events, safe=False)

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



    