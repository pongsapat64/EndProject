from django.db import models
from studentapp.models import *

# Create your models here.
    
class Lecturer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

class Adviser(models.Model):
    lecturer = models.ForeignKey(Lecturer, on_delete=models.CASCADE, blank=True, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, blank=True, null=True)

class Committee(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=True, null=True)
    lecturer = models.ForeignKey(Lecturer, on_delete=models.CASCADE, blank=True, null=True)

class Comadviser(models.Model):
    committee = models.ForeignKey(Committee, on_delete=models.CASCADE, null=True)
    adviser = models.ForeignKey(Adviser, on_delete=models.CASCADE, null=True)

class TimeSlot(models.Model):
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"Appointment: {self.date.strftime('%Y-%m-%d')} {self.start_time.strftime('%I:%M %p')} - {self.end_time.strftime('%I:%M %p')}"

class AvailableTime(models.Model):
    lecturer = models.ForeignKey(Lecturer, on_delete=models.CASCADE, blank=True, null=True)
    timeslot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE, blank=True, null=True)

class Appointment(models.Model):
    comadviser = models.ForeignKey(Comadviser, on_delete=models.CASCADE, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, blank=True, null=True)
    availabletime = models.ForeignKey(AvailableTime,on_delete=models.CASCADE, blank=True, null=True)

class Result(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, blank=True, null=True)

class ScoreForm(models.Model):
    comadviser = models.ForeignKey(Comadviser, on_delete=models.CASCADE, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, blank=True, null=True)

class ProjectManager(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, blank=True, null=True)
    comadviser = models.ForeignKey(Comadviser, on_delete=models.CASCADE, null=True)

class Role(models.Model):
    DEFAULT_ROLES = ['Admin', 'Lecturer', 'Student', 'Adviser', 'Committee']

    name = models.CharField(max_length=50, default=DEFAULT_ROLES[0], choices=[(role, role) for role in DEFAULT_ROLES])
    users = models.ManyToManyField(User, related_name='roles', blank=True)

    def str(self):
        return self.name



