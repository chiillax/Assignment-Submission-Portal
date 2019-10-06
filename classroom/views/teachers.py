from django.views.generic import TemplateView
from django.shortcuts import render
from django.http import HttpResponse
from classroom.models import Student, Teacher, User, Assignment
from ..forms import TeacherSignUpForm, StudentSignUpForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import (CreateView, DeleteView, DetailView, ListView, UpdateView)
from ..decorators import teacher_required
from django.utils.decorators import method_decorator


class TeacherSignUpView(CreateView):
    model = User
    form_class = TeacherSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'teacher'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('teachers:assignments_list')


@method_decorator([login_required, teacher_required], name='dispatch')
class AssignmentListView(ListView):
    model = Assignment
    ordering = ('createdTime',)
    context_object_name = 'assignments'
    template_name = 'classroom/teachers/assignments.html'

    def get_queryset(self):
        queryset = Assignment.objects.filter(postBy__user=self.request.user)
        return queryset
