from classroom.models import Teacher, User, Assignment, Solution
from ..forms import TeacherSignUpForm, AssignmentCreateForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import (CreateView, DeleteView, DetailView, ListView, UpdateView)
from ..decorators import teacher_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.db.models import Count
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from classroom.tokens import account_activation_token
from django.core.mail import EmailMessage


class TeacherSignUpView(CreateView):
    model = User
    form_class = TeacherSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'teacher'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        # user = form.save()
        # login(self.request, user)
        user = form.save()
        user.is_active = False
        user.save()
        current_site = get_current_site(self.request)
        mail_subject = 'Activate your account.'
        message = render_to_string('registration/account_activation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
            'token': account_activation_token.make_token(user),
        })
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()
        return render(self.request, 'registration/account_activation_confirm.html', {'form': form})
        # return redirect('teachers:assignments_list')


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
    # fields = ('course', 'semester', 'name', 'description', 'dueDate', 'isLateAllowed', 'file', )
    form_class = AssignmentCreateForm
    template_name = 'classroom/teachers/assignment_add_form.html'

    def form_valid(self, form):
        assignment = form.save(commit=False)
        assignment.postBy = self.request.user.teacher
        assignment.save()
        messages.success(self.request, 'Assignment is posted successfully.')
        return redirect('teachers:assignment_detail', assignment.pk)


@method_decorator([login_required, teacher_required], name='dispatch')
class AssignmentUpdateView(UpdateView):
    model = Assignment
    # fields = ('course', 'semester', 'name', 'description', 'dueDate', 'isLateAllowed', 'file', )
    form_class = AssignmentCreateForm
    context_object_name = 'assignment'
    template_name = 'classroom/teachers/assignment_change_form.html'

    def get_success_url(self):
        messages.success(self.request, 'Assignment is updated successfully.')
        return reverse('teachers:assignment_detail', kwargs={'pk': self.object.pk})


@method_decorator([login_required, teacher_required], name='dispatch')
class AssignmentSolutionsView(DetailView):
    model = Assignment
    context_object_name = 'assignment'
    template_name = 'classroom/teachers/assignment_solutions.html'

    def get_context_data(self, **kwargs):
        assignment = self.get_object()
        kwargs['submissions'] = Solution.objects.filter(assignment=assignment).order_by('-submissionTime')
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        return self.request.user.teacher.assignments


@method_decorator([login_required, teacher_required], name='dispatch')
class AssignmentDetailView(DetailView):
    model = Assignment
    context_object_name = 'assignment'
    template_name = 'classroom/teachers/assignment_detail.html'

    def get_context_data(self, **kwargs):
        assignment = self.get_object()
        kwargs['submissions'] = len(Solution.objects.filter(assignment=assignment))
        return super().get_context_data(**kwargs)

    # def get_success_url(self):
    #     return reverse_lazy('teachers:assignment_detail', kwargs={'pk': self.object.pk})


@method_decorator([login_required, teacher_required], name='dispatch')
class AssignmentDeleteView(DeleteView):
    model = Assignment
    context_object_name = 'assignment'
    template_name = 'classroom/teachers/assignment_delete.html'
    success_url = reverse_lazy('teachers:assignments_list')

    def test_func(self):
        obj = self.get_object()
        return obj.user.teacher == self.request.user.teacher

