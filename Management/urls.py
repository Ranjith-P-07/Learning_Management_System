from django.urls import path
from . import views

urlpatterns = [
    path('courses/', views.CoursesAPIView.as_view(), name='courses'),
    path('course-update/<int:id>/', views.CourseUpdateAPIView.as_view(), name='course_update'),
    path('mentor-list/', views.MentorAPIView.as_view(), name='mentor_List'),
    path('mentor_update/<int:id>/', views.MentorUpdateAPIView.as_view(), name='mentor_update'),
]