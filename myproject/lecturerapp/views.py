from django.http import HttpResponse
from django.shortcuts import redirect, render
from mysite.models import AvailableTime
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

@user_passes_test(is_Lecturer)
@login_required(login_url='/mysite/login')
def addtime_select(request, year=None, month=None, day=None):
    try:
        if year is None or month is None or day is None:
            # If the date is not specified, use the current date
            now = datetime.now()
            year, month, day = now.year, now.month, now.day

        if request.method == 'POST':
            form = TimeSlotForm(request.POST)
            if form.is_valid():
                selected_time_slots = form.cleaned_data.get('time_slot')
                for time_slot in selected_time_slots:
                    # Create or update AvailableTime instance
                    available_time, created = AvailableTime.objects.get_or_create(date=datetime(year, month, day))
                    # Create TimeSlot instance and link to AvailableTime
                    TimeSlot.objects.create(
                        available_time=available_time,
                        start_time=time_slot[0],  # Assuming time_slot is a tuple (start_time, end_time)
                        end_time=time_slot[1],
                        date=datetime(year, month, day)
                    )
                # After processing, redirect to another page or render a different template
                return redirect('addtime.html', year=year, month=month, day=day)
        else:
            # Fetch available time slots for the given date
            available_time_slots = AvailableTime.objects.filter(date=datetime(year, month, day))
            time_choices = [(slot.start_time, slot.end_time) for slot in available_time_slots]
            form = TimeSlotForm(time_choices=time_choices)

    except ZeroDivisionError:
        return HttpResponse("Error: Division by zero")

    except Exception as e:
        # Handle other exceptions
        return HttpResponse(f"An error occurred: {e}")

    return render(request, 'addtimeselect.html', {'form': form, 'year': year, 'month': month, 'day': day})

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
    