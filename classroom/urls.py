from django.urls import path, include
from .views import classroom, students, teachers

# from .views import homePageView
# from .views import HomePageView

urlpatterns = [
    # path('', HomePageView.as_view(), name='home'),
    path('', classroom.home, name='home'),
    path('ajax/load-courses/', classroom.load_courses, name='ajax_load_courses'),
    path('students/', include(([
        path('assignments', students.AssignmentListView.as_view(), name='assignments_list'),
        path('assignments/<int:pk>/detail/', students.AssignmentDetailView.as_view(), name='assignment_detail'),
        path('update/courses/', students.StudentCoursesView.as_view(), name='update_courses'),
        path('assignments/<int:pk>/solution/', students.SolutionAddView.as_view(), name='solution_add'),
    ], 'classroom'), namespace='students')),

    path('teachers/', include(([
        path('assignments', teachers.AssignmentListView.as_view(), name='assignments_list'),
        path('assignment/add/', teachers.AssignmentCreateView.as_view(), name='assignment_add'),
        path('assignment/<int:pk>/edit/', teachers.AssignmentUpdateView.as_view(), name='assignment_edit'),
        path('assignment/<int:pk>/delete/', teachers.AssignmentDeleteView.as_view(), name='assignment_delete'),
        path('assignments/<int:pk>/solutions/', teachers.AssignmentSolutionsView.as_view(), name='assignment_solutions'),
        path('assignments/<int:pk>/', teachers.AssignmentDetailView.as_view(), name='assignment_detail'),
    ], 'classroom'), namespace='teachers')),
]
