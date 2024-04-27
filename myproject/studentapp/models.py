from django.db import models
from mysite.models import *
from django.contrib.auth.models import User

# Create your models here.
class Project(models.Model):
    topic = models.CharField(max_length=100, null=True, blank=True)
    document = models.CharField(max_length=300, null=True, blank=True)
    presentationSlide = models.CharField(max_length=300, null=True, blank=True)
    year = models.CharField(max_length=5, null=True, blank=True)

    def __str__(self) -> str:
        return f' topic:{self.topic} document:{self.document} slide:{self.presentationSlide} year:{self.year}'

class Student(models.Model):
    student_project = models.ForeignKey(Project, on_delete=models.DO_NOTHING, null=True, blank=True)
    student_id = models.CharField(max_length=11, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.student_id}"
    

    

 