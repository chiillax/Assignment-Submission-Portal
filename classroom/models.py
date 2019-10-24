from django.db import models
from django.contrib.auth.models import AbstractUser
import os
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime


class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    email = models.EmailField(unique=True, null=False, blank=False)


class Semester(models.Model):
    semester = models.PositiveSmallIntegerField(default=1, validators=[MaxValueValidator(10), MinValueValidator(1)], unique=True)
    startTime = models.DateTimeField(default=datetime.now())

    class Meta:
        ordering = ('semester',)

    def __str__(self):
        return str(self.semester)


class Course(models.Model):
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    name = models.CharField(max_length=10)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    semester = models.ForeignKey(Semester, on_delete=models.SET_NULL, null=True)
    courses = models.ManyToManyField(Course, related_name='taken_students')

    def __str__(self):
        return self.user.username


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.user.username


def file_size(value):
    limit = 10 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 10 MB.')


class Assignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    semester = models.ForeignKey(Semester, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    file = models.FileField(upload_to='media/Assignments', blank=True, null=True, validators=[file_size])
    createdTime = models.DateTimeField(auto_now_add=True)
    dueDate = models.DateTimeField()
    postBy = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='assignments')
    isLateAllowed = models.BooleanField(default=False)

    class Meta:
        ordering = ('createdTime',)

    def __str__(self):
        return self.name

    def file_url(self):
        return self.file.url

    def file_name(self):
        return self.file.url[25:]


class Solution(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='solutions')
    submittedBy = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='solutions')
    file = models.FileField(upload_to='media/Solutions', validators=[file_size])
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
