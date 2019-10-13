from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import Assignment
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
        Student.objects.create(user=user, semester=self.cleaned_data.get('semester'))
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
        Teacher.objects.create(user=user)
        return user


class AssignmentCreateForm(forms.ModelForm):
    class Meta:
        model = Assignment
        # fields = ['name', 'start_date', 'end_date']
        fields = ['course', 'semester', 'name', 'description', 'dueDate', 'isLateAllowed', 'file', ]
        widgets = {
            'dueDate': forms.DateTimeInput(attrs={"placeholder" : "YYYY-MM-DD HH:mm (24 hours format)"})
        }

