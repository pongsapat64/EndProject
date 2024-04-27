from django.db import models
from studentapp.models import *
from studentapp.models import Student
from django.contrib.auth.models import User

# Create your models here.
    
class Lecturer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Adviser(models.Model):
    lecturer = models.ForeignKey(Lecturer, on_delete=models.CASCADE, blank=True, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, blank=True, null=True)

class Appointment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    committee = models.ForeignKey(Lecturer, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    summary = models.CharField(max_length=100)

    def __str__(self):
        return self.summary
    

class TimeSlot(models.Model):
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)


class AvailableTime(models.Model):
    lecturer = models.ForeignKey(Lecturer, on_delete=models.CASCADE, blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    

class Score(models.Model):
    student = models.ForeignKey(Student, null=True, on_delete=models.CASCADE)
    lecturer = models.ForeignKey(Lecturer, null=True, on_delete=models.CASCADE)
    scored = models.IntegerField(null=True)
    maxscore = models.IntegerField(default=10)


class Role(models.Model):
    DEFAULT_ROLES = ['Admin', 'Lecturer', 'Student', 'Adviser', 'Committee']

    name = models.CharField(max_length=50, default=DEFAULT_ROLES[0], choices=[(role, role) for role in DEFAULT_ROLES])
    users = models.ManyToManyField(User, related_name='roles', blank=True)

    def __str__(self):
        user_names = ', '.join([user.username for user in self.users.all()])
        return f"{user_names} is {self.name} "

    





