from django.contrib import admin
from .models import User, Assignment, Solution, Student, Teacher, Semester, Course

# admin.site.register(User)
admin.site.register(Solution)
# admin.site.register(Student)
# admin.site.register(Teacher)
# admin.site.register(Course)


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'user_type']

    class Meta:
        model = Student

    def user_type(self, obj):
        if obj.is_student:
            return 'student'
        return 'teacher'


class StudentAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_email', 'semester']
    ordering = ['semester']

    class Meta:
        model = Student

    def get_email(self, obj):
        return obj.user.email


class TeacherAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_email']
    ordering = ['-user']

    class Meta:
        model = Teacher

    def get_email(self, obj):
        return obj.user.email


class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'course', 'postBy', 'createdTime']
    ordering = ['-createdTime']

    class Meta:
        model = Assignment


class SemesterAdmin(admin.ModelAdmin):
    list_display = ['semester', 'startTime']
    ordering = ['semester']

    class Meta:
        model = Semester


class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'semester']
    ordering = ['semester', 'name']

    class Meta:
        model = Course


admin.site.register(User, UserAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Assignment, AssignmentAdmin)
admin.site.register(Semester, SemesterAdmin)
admin.site.register(Course, CourseAdmin)
