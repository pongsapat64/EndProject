from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    topic = models.CharField(max_length=100, null=True, blank=True)
    document = models.CharField(max_length=300, null=True, blank=True)
    presentationSlide = models.CharField(max_length=300, null=True, blank=True)
    year = models.CharField(max_length=5, null=True, blank=True)

    def __str__(self) -> str:
        return f' topic:{self.topic} document:{self.document} slide:{self.presentationSlide} year:{self.year}'

class Student(models.Model):
    student_project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    student_id = models.IntegerField(null=True, blank=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    subject = models.CharField(max_length=100, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.student_id}"
    
class Lecturer(models.Model):
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Adviser(models.Model):
    lecturer = models.ForeignKey(Lecturer, on_delete=models.CASCADE, blank=True, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"Adviser: {self.lecturer} - {self.student}"

class Appointment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    committee = models.ForeignKey(Lecturer, on_delete=models.CASCADE, null=True)
    adviser = models.ForeignKey(Adviser, on_delete=models.CASCADE, blank=True, null=True)
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    summary = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.summary

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

    





