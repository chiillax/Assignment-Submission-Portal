from django.urls import path, include
from .views import classroom, students, teachers

# from .views import homePageView
# from .views import HomePageView

urlpatterns = [
    # path('', HomePageView.as_view(), name='home'),
    path('', classroom.home, name='home'),
    path('students/', include(([
        path('', students.AssignmentListView.as_view(), name='assignments_list'),
        path('assignments/<int:pk>/detail/', students.AssignmentDetailView.as_view(), name='assignment_detail'),
        path('assignments/<int:pk>/solution/', students.SolutionAddView.as_view(), name='solution_add'),
    ], 'classroom'), namespace='students')),

    path('teachers/', include(([
        path('', teachers.AssignmentListView.as_view(), name='assignments_list'),
        path('assignment/add/', teachers.AssignmentCreateView.as_view(), name='assignment_add'),
        path('assignment/<int:pk>/edit', teachers.AssignmentUpdateView.as_view(), name='assignment_edit'),
        # path('quiz/<int:pk>/delete/', teachers.QuizDeleteView.as_view(), name='quiz_delete'),
        path('assignments/<int:pk>/solutions/', teachers.AssignmentSolutionsView.as_view(), name='assignment_solutions'),
        path('assignments/<int:pk>/', teachers.AssignmentDetailView.as_view(), name='assignment_detail'),
    ], 'classroom'), namespace='teachers')),
]
