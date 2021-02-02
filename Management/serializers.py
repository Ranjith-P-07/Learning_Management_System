from rest_framework import serializers
from .models import Course, Mentor


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class MentorSerializer(serializers.ModelSerializer):
    mentor = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Mentor
        fields = ['mentor', 'course']
