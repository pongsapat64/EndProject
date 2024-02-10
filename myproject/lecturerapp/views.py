from django.http import HttpResponse
from django.shortcuts import redirect, render
from mysite.models import Lecturer
from studentapp.forms import LoginForm, RegisterForm, UserProfileForm
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
                        return render(req,'editprofileLec.html',{'user':user})
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
    return render(req, 'editprofileLec.html', {'form': form})
    