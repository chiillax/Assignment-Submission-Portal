from django.db import models
from django.contrib.auth.models import AbstractUser
import os
from django.conf import settings


class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    email = models.EmailField(unique=True, null=False, blank=False)


class Student(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    semester = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.user.username


class Teacher(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.user.username


class Assignment(models.Model):
    course = models.CharField(max_length=8)
    semester = models.IntegerField()
    name = models.CharField(max_length=255)
    description = models.TextField()
    file = models.FileField(upload_to='media/Assignments')
    createdTime = models.DateTimeField(auto_now_add=True)
    dueDate = models.DateTimeField()
    postBy = models.ForeignKey(
        Teacher, on_delete=models.CASCADE, related_name='assignments')
    isLateAllowed = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def file_url(self):
        return self.file.url

    def file_name(self):
        return self.file.url[25:]


class Solution(models.Model):
    assignment = models.ForeignKey(
        Assignment, on_delete=models.CASCADE, related_name='solutions')
    submittedBy = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='solutions')
    file = models.FileField(upload_to='media/Solutions')
    submissionTime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.submittedBy.user.username

    def file_url(self):
        return self.file.url

    def file_name(self):
        return self.file.url[23:]

    def delete(self, *args, **kwargs):
        os.remove(os.path.join(settings.MEDIA_ROOT, self.file.name))
        super(Solution, self).delete(*args, **kwargs)
