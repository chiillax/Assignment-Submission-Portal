from django.db import models
from django.contrib.auth.models import AbstractUser


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
    file = models.FileField()
    createdTime = models.DateTimeField(auto_now_add=True)
    dueDate = models.DateTimeField()
    postBy = models.ForeignKey(
        Teacher, on_delete=models.CASCADE, related_name='assignments')
    isLateAllowed = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Solution(models.Model):
    assignment = models.ForeignKey(
        Assignment, on_delete=models.CASCADE, related_name='solutions')
    submittedBy = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='solutions')
    submissionTime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.submittedBy.user.username
