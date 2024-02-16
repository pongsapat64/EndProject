from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Lecturer, TimeSlot
from studentapp.models import Student


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")

class LecturerProfileForm(forms.ModelForm):
    class Meta:
        model = Lecturer
        fields = ('first_name', "last_name")

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('first_name', "last_name")

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=150)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

class SelectForm(forms.Form):
    items = forms.ModelMultipleChoiceField(queryset=Lecturer.objects.all(), widget=forms.CheckboxSelectMultiple)


class TimeSlotForm(forms.Form):
    time_slot = forms.MultipleChoiceField(
        choices=[],
        widget=forms.CheckboxSelectMultiple
    )

    def __init__(self, *args, **kwargs):
        time_choices = kwargs.pop('time_choices', [])
        super(TimeSlotForm, self).__init__(*args, **kwargs)
        self.fields['time_slot'].choices = time_choices
