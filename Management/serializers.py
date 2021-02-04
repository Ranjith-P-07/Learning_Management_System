from rest_framework import serializers
from .models import Course, Mentor, Student, Education, StudentCourseMentor


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class MentorSerializer(serializers.ModelSerializer):
    mentor = serializers.StringRelatedField(read_only=True)
    course = serializers.StringRelatedField(read_only=True, many=True)

    class Meta:
        model = Mentor
        fields = '__all__'


class MentorUpdateSerializer(serializers.ModelSerializer):
    mentor = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Mentor
        fields = ['mentor', 'course']


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


class StudentEducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = '__all__'


class StudentCourseMentorSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentCourseMentor
        fields = ['student', 'course', 'mentor', 'create_by']
        extra_kwargs = {'course': {'required': True}, 'mentor': {'required': True}, 'create_by': {'read_only': True}}

    def validate(self, data):
        data['create_by'] = self.context['user']
        return data


class StudentCourseMentorReadSerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField(read_only=True)
    mentor = serializers.StringRelatedField(read_only=True)
    course = serializers.StringRelatedField(read_only=True)
    create_by = serializers.StringRelatedField(read_only=True)
    updated_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = StudentCourseMentor
        fields = "__all__"


class StudentCourseMentorUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentCourseMentor
        fields = ['course', 'mentor', 'updated_by']
        extra_kwargs = {'course': {'required': True}, 'mentor': {'required': True}, 'updated_by': {'read_only': True}}

    def validate(self, data):
        data['updated_by'] = self.context['user']
        return data