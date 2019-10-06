from django.contrib import admin
from .models import User, Assignment, Solution, Student, Teacher

admin.site.register(User)
admin.site.register(Assignment)
admin.site.register(Solution)
admin.site.register(Student)
admin.site.register(Teacher)
