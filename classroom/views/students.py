from django.views.generic import TemplateView
from django.shortcuts import render
from django.http import HttpResponse
from classroom.models import Student, Teacher, User
from ..forms import TeacherSignUpForm, StudentSignUpForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import CreateView, ListView, UpdateView
from ..decorators import student_required
from django.utils.decorators import method_decorator
from classroom.models import Student, Teacher, User, Assignment



class StudentSignUpView(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('students:assignments_list')


@method_decorator([login_required, student_required()], name='dispatch')
class AssignmentListView(ListView):
    model = Assignment
    ordering = ('createdTime',)
    context_object_name = 'assignments'
    template_name = 'classroom/students/assignments.html'

    def get_queryset(self):
        queryset = Assignment.objects.filter(semester=self.request.user.student.semester)
        return queryset
