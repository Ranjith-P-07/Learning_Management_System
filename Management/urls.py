from django.urls import path
from . import views

urlpatterns = [
    path('courses/', views.CoursesAPIView.as_view(), name='courses'),
    path('course-update/<int:id>/', views.CourseUpdateAPIView.as_view(), name='course_update'),
    path('mentor-list/', views.MentorAPIView.as_view(), name='mentor_List'),
    path('mentor-update/<int:id>/', views.MentorUpdateAPIView.as_view(), name='mentor_update'),
    path('student-personal/<int:id>/', views.StudentPersonalDetailAPIView.as_view(), name='student_update'),
    path('student-education/<int:id>/', views.StudentEducationAPIView.as_view(), name='student-education'),
    path('student-course-mentor/', views.StudentCourseMentorMapAPIView.as_view(), name='student-course-mentor'),
    path('student-course-mentor-update/<int:id>/', views.StudentCourseMentorUpdateAPIView.as_view(), name='student-course-mentor-update'),
]