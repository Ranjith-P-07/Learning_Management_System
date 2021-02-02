from django.shortcuts import render
from django.utils.decorators import method_decorator
from rest_framework.generics import GenericAPIView
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import CourseSerializer, MentorSerializer
from .models import Course, Mentor
from django.contrib.auth.decorators import login_required
import sys

sys.path.append('..')
from Register.permissions import Admin_validate


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
class MentorUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MentorSerializer
    permission_classes = (Admin_validate,)
    queryset = Mentor.objects.all()
    lookup_field = 'id'

    def perform_update(self, serializer):
        serializer.save()
        return Response({'response': 'Mentor detail is updated'}, status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        instance.delete()
        return Response({'response': 'Mentor is deleted'}, status=status.HTTP_204_NO_CONTENT)
