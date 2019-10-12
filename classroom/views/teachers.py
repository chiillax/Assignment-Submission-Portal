from classroom.models import Teacher, User, Assignment, Solution
from ..forms import TeacherSignUpForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import (CreateView, DeleteView, DetailView, ListView, UpdateView)
from ..decorators import teacher_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.db.models import Count


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
    ordering = ('-createdTime',)
    context_object_name = 'assignments'
    template_name = 'classroom/teachers/assignments.html'

    def get_context_data(self, **kwargs):
        kwargs['assignments'] = Assignment.objects.filter(postBy__user=self.request.user).annotate(num_solution=Count('solutions')).order_by('-createdTime')
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        queryset = Assignment.objects.filter(postBy__user=self.request.user).order_by('-createdTime')
        return queryset


@method_decorator([login_required, teacher_required], name='dispatch')
class AssignmentCreateView(CreateView):
    model = Assignment
    fields = ('course', 'semester', 'name', 'description', 'dueDate', 'isLateAllowed', 'file', )
    template_name = 'classroom/teachers/assignment_add_form.html'

    def form_valid(self, form):
        assignment = form.save(commit=False)
        assignment.postBy = self.request.user.teacher
        assignment.save()
        messages.success(self.request, 'Assignment is posted successfully.')
        return redirect('teachers:assignment_change', assignment.pk)


@method_decorator([login_required, teacher_required], name='dispatch')
class AssignmentUpdateView(UpdateView):
    model = Assignment
    fields = ('course', 'semester', 'name', 'description', 'dueDate', 'isLateAllowed', 'file', )
    context_object_name = 'assignment'
    template_name = 'classroom/teachers/assignment_change_form.html'

    # def get_context_data(self, **kwargs):
    #     # kwargs['questions'] = self.get_object().questions.annotate(answers_count=Count('answers'))
    #     kwargs[]
    #     return super().get_context_data(**kwargs)

    def get_queryset(self):
        '''
        This method is an implicit object-level permission management
        This view will only match the ids of existing quizzes that belongs
        to the logged in user.
        '''
        return self.request.user.teacher.assignments.all()

    def get_success_url(self):
        return reverse('teachers:assignment_change', kwargs={'pk': self.object.pk})


@method_decorator([login_required, teacher_required], name='dispatch')
class AssignmentDetailView(DetailView):
    model = Assignment
    context_object_name = 'assignment'
    template_name = 'classroom/teachers/assignment_solutions.html'

    def get_context_data(self, **kwargs):
        assignment = self.get_object()
        kwargs['submissions'] = Solution.objects.filter(assignment=assignment).order_by('-submissionTime')
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        return self.request.user.teacher.assignments

