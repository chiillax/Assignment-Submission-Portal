from django.urls import path, include
from .views import classroom, students, teachers

# from .views import homePageView
# from .views import HomePageView

urlpatterns = [
    # path('', homePageView, name='home')
    # path('', HomePageView.as_view(), name='home'),
    path('', classroom.home, name='home'),
    path('students/', include(([
        path('', students.AssignmentListView.as_view(), name='assignments_list'),
        path('assignments/<int:pk>/detail/', students.AssignmentDetailView.as_view(), name='assignment_detail'),
        path('assignments/<int:pk>/solution/', students.SolutionAddView.as_view(), name='solution_add'),
        # path('interests/', students.StudentInterestsView.as_view(), name='student_interests'),
        # path('taken/', students.TakenQuizListView.as_view(), name='taken_quiz_list'),
        # path('quiz/<int:pk>/', students.take_quiz, name='take_quiz'),
    ], 'classroom'), namespace='students')),

    path('teachers/', include(([
        path('', teachers.AssignmentListView.as_view(), name='assignments_list'),
        path('assignment/add/', teachers.AssignmentCreateView.as_view(), name='assignment_add'),
        path('assignment/<int:pk>/', teachers.AssignmentUpdateView.as_view(), name='assignment_change'),
        # path('quiz/<int:pk>/delete/', teachers.QuizDeleteView.as_view(), name='quiz_delete'),
        path('assignments/<int:pk>/solutions/', teachers.AssignmentDetailView.as_view(), name='assignment_solutions'),
        # path('quiz/<int:pk>/question/add/', teachers.question_add, name='question_add'),
        # path('quiz/<int:quiz_pk>/question/<int:question_pk>/', teachers.question_change, name='question_change'),
        # path('quiz/<int:quiz_pk>/question/<int:question_pk>/delete/', teachers.QuestionDeleteView.as_view(), name='question_delete'),
    ], 'classroom'), namespace='teachers')),
]
