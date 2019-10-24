from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import Assignment
from classroom.models import Student, Teacher, User, Course


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
            'dueDate': forms.DateTimeInput(attrs={"placeholder" : "MM-DD-YYYY HH:mm (24 hours format)"})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['course'].queryset = Course.objects.none()

        if 'semester' in self.data:
            try:
                semester_id = int(self.data.get('semester'))
                self.fields['course'].queryset = Course.objects.filter(semester_id=semester_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['course'].queryset = self.instance.semester.course_set.order_by('name')


class StudentCoursesForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('semester', 'courses', )
        # widgets = {
        #     'courses': forms.CheckboxSelectMultiple
        # }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['courses'].queryset = Course.objects.none()

        if 'semester' in self.data:
            try:
                semester_id = int(self.data.get('semester'))
                self.fields['courses'].queryset = Course.objects.filter(semester_id=semester_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['courses'].queryset = self.instance.semester.course_set.order_by('name')

