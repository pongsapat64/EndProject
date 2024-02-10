from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Student


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name")

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=150)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
