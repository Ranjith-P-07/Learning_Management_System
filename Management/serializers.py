from rest_framework import serializers
from .models import Course, Mentor, Student


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class MentorSerializer(serializers.ModelSerializer):
    mentor = serializers.StringRelatedField(read_only=True)
    course = serializers.StringRelatedField(read_only=True, many=True)

    class Meta:
        model = Mentor
        fields = ['mentor', 'course']


class MentorUpdateSerializer(serializers.ModelSerializer):
    mentor = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Mentor
        fields = ['mentor', 'course']


