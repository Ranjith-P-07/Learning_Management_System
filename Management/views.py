from django.shortcuts import render
from django.utils.decorators import method_decorator
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import CourseSerializer, MentorSerializer, MentorUpdateSerializer, StudentSerializer
from .models import Course, Mentor, Student
from django.contrib.auth.decorators import login_required
import sys

sys.path.append('..')
from Register.permissions import Admin_validate, Mentor_validate, Student_validate


@method_decorator(login_required(login_url='/user/login/'), name='dispatch')
class CoursesAPIView(generics.ListCreateAPIView):
    serializer_class = CourseSerializer
    permission_classes = (Admin_validate,)

    def get_queryset(self):
        queryset = Course.objects.all()
        return queryset

    def perform_create(self, serializer):
        serializer.save()
        return Response({'response': 'Course is successfully added'}, status=status.HTTP_201_CREATED)


@method_decorator(login_required(login_url='/user/login/'), name='dispatch')
class CourseUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CourseSerializer
    permission_classes = (Admin_validate,)
    queryset = Course.objects.all()
    lookup_field = 'id'

    def perform_update(self, serializer):
        serializer.save()
        return Response({'response': 'Course is updated'}, status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        instance.delete()
        return Response({'response': 'Course is deleted'}, status=status.HTTP_204_NO_CONTENT)


@method_decorator(login_required(login_url='/user/login/'), name='dispatch')
class MentorAPIView(generics.ListAPIView):
    serializer_class = MentorSerializer
    permission_classes = (Admin_validate,)

    queryset = Mentor.objects.all()


@method_decorator(login_required(login_url='/user/login/'), name='dispatch')
class MentorUpdateAPIView(GenericAPIView):
    serializer_class = MentorUpdateSerializer
    permission_classes = (Admin_validate,)
    queryset = Mentor.objects.all()

    def get(self, request, id):
        try:
            mentor = self.queryset.get(id=id)
            serializer = MentorSerializer(mentor)
            return Response({'response': serializer.data}, status=status.HTTP_200_OK)
        except:
            return Response({'response': 'Mentor not found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, id):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            mentor = self.queryset.get(id=id)
        except Mentor.DoesNotExist:
            return Response({'response': 'Mentor id does not exist'}, status=status.HTTP_404_NOT_FOUND)
        for course_id in serializer.data.get('course'):
            for mentor_course in mentor.course.all():
                if course_id == mentor_course.id:
                    return Response({'response': 'This course is already added'}, status=status.HTTP_400_BAD_REQUEST)
                mentor.course.add(course_id)
                return Response({'response': f" New course is/are added to {mentor}'s course list"})

    def delete(self, request, id):
        try:
            mentor = self.queryset.get(id=id)
            mentor.delete()
            return Response({'response': 'Mentor is deleted successfully!!'}, status=status.HTTP_200_OK)
        except:
            return Response({'response': 'Mentor not found'}, status=status.HTTP_404_NOT_FOUND)


