from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.contrib import admin
from .models import *


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")

class UserCreateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "password", 'email')


class LecturerProfileForm(forms.ModelForm):
    class Meta:
        model = Lecturer
        fields = ('first_name', "last_name")

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('first_name', "last_name", "student_id", "subject")

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=150)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

class TimeSlotForm(forms.Form):
    time_slot = forms.MultipleChoiceField(
        choices=[],
        widget=forms.CheckboxSelectMultiple
    )

    def __init__(self, *args, **kwargs):
        time_choices = kwargs.pop('time_choices', [])
        super(TimeSlotForm, self).__init__(*args, **kwargs)
        self.fields['time_slot'].choices = time_choices

class AdviserAdminForm(forms.ModelForm):
    class Meta:
        model = Adviser
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['lecturer'].queryset = Lecturer.objects.all()  # ตั้งค่า queryset ของ lecturer เพื่อให้ admin เลือก

class AdviserAdmin(admin.ModelAdmin):
    form = AdviserAdminForm
    list_display = ['lecturer', 'student']