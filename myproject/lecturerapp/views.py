from django.http import HttpResponse
from django.shortcuts import redirect, render
from mysite.models import Lecturer
from studentapp.forms import LoginForm, RegisterForm, UserProfileForm, LecturerProfileForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User

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
def addtime(req):
    return render(req, "addtime.html")


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
    