from django.contrib import admin
from .models import Course, Mentor, Student, Performance, Education, StudentCourseMentor

admin.site.register(Course)
admin.site.register(Mentor)
admin.site.register(Student)
admin.site.register(Education)
admin.site.register(Performance)
admin.site.register(StudentCourseMentor)

