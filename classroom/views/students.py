from ..forms import StudentSignUpForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import CreateView, ListView, UpdateView, DetailView
from ..decorators import student_required
from django.utils.decorators import method_decorator
from classroom.models import Student, User, Assignment, Solution
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Count, Q
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from classroom.tokens import account_activation_token
from django.core.mail import EmailMessage


class StudentSignUpView(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
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
        # return HttpResponse('Please confirm your email address to complete the registration')
        # return redirect('students:assignments_list')


@method_decorator([login_required, student_required()], name='dispatch')
class AssignmentListView(ListView):
    model = Assignment
    ordering = ('createdTime',)
    context_object_name = 'assignments'
    template_name = 'classroom/students/assignments.html'

    def get_context_data(self, **kwargs):
        # highly_rated = Count('book', filter=Q(book__rating__gte=7))
        # Author.objects.annotate(num_books=Count('book'), highly_rated_books=highly_rated)

        isDone = Count('solutions', filter=Q(solutions__submittedBy=self.request.user.student))
        kwargs['assignments'] = Assignment.objects.filter(semester=self.request.user.student.semester).annotate(num_solution=Count('solutions'), done=isDone).order_by('-createdTime')
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        queryset = Assignment.objects.filter(semester=self.request.user.student.semester).order_by('-createdTime')
        return queryset


@method_decorator([login_required, student_required], name='dispatch')
class AssignmentDetailView(DetailView):
    model = Assignment
    context_object_name = 'assignment'
    template_name = 'classroom/students/assignment_detail.html'

    def get_context_data(self, **kwargs):
        assignment = self.get_object()
        issubmitted = None
        issubmitted = Solution.objects.filter(assignment=assignment, submittedBy=self.request.user.student)
        kwargs['issubmitted'] = 0
        if len(issubmitted) != 0:
            # print(issubmitted)
            kwargs['issubmitted'] = 1
            kwargs['solution'] = Solution.objects.filter(assignment=assignment, submittedBy=self.request.user.student)[0]
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        return reverse_lazy('students:assignment_detail', kwargs={'pk': self.object.pk})
    # def get_queryset(self):
    #     queryset = Assignment.objects.filter(pk=pk)
    #     return queryset


@method_decorator([login_required, student_required], name='dispatch')
class SolutionAddView(CreateView):
    model = Solution
    fields = ('file', )
    template_name = 'classroom/students/solution_add_form.html'

    def get_context_data(self, **kwargs):
        kwargs['assignment'] = Assignment.objects.get(pk=self.kwargs['pk'])
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        assignment = Assignment.objects.get(pk=self.kwargs['pk'])
        sol = Solution.objects.filter(assignment=assignment, submittedBy=self.request.user.student)
        sol_id = 0
        if len(sol) != 0:
            sol_id = sol[0].pk
        solution = form.save(commit=False)
        solution.submittedBy = self.request.user.student
        solution.assignment = assignment
        solution.save()
        if sol_id != 0:
            s = get_object_or_404(Solution, pk=sol_id)
            s.delete()
        messages.success(self.request, 'Solution is posted successfully.')
        return redirect('students:assignment_detail', pk=self.kwargs['pk'])

