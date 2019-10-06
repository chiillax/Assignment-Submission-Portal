from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from classroom.models import Student, Teacher, User


class StudentSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    semester = forms.IntegerField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.email = self.cleaned_data.get('email')
        user.save()
        student = Student.objects.create(user=user, semester=self.cleaned_data.get('semester'))
        return user


class TeacherSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_teacher = True
        user.email = self.cleaned_data.get('email')
        user.save()
        teacher = Teacher.objects.create(user=user)
        return user
