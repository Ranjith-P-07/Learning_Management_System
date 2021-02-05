from rest_framework import serializers
from .models import Course, Mentor, Student, Education, StudentCourseMentor


class CourseSerializer(serializers.ModelSerializer):
    """
        This Serializer is used for Course data Serializing Purpose
    """
    class Meta:
        model = Course
        fields = '__all__'


class MentorSerializer(serializers.ModelSerializer):
    """
        This Serializer is used for Mentor data Serializing Purpose
    """
    mentor = serializers.StringRelatedField(read_only=True)
    course = serializers.StringRelatedField(read_only=True, many=True)

    class Meta:
        model = Mentor
        fields = '__all__'


class MentorUpdateSerializer(serializers.ModelSerializer):
    """
        This Serializer is used for MentorUpdated data Serializing Purpose
    """
    mentor = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Mentor
        fields = ['mentor', 'course']


class StudentSerializer(serializers.ModelSerializer):
    """
        This Serializer is used for Student Data Serializing Purpose
    """
    class Meta:
        model = Student
        fields = '__all__'


class StudentEducationSerializer(serializers.ModelSerializer):
    """
        This Serializer is used for StudentEducation data serializing Purpose
    """
    class Meta:
        model = Education
        fields = '__all__'


class StudentCourseMentorSerializer(serializers.ModelSerializer):
    """
        This Serializer is used for StudentCourseMentor Data Serializing Purpose
    """
    class Meta:
        model = StudentCourseMentor
        fields = ['student', 'course', 'mentor', 'create_by']
        extra_kwargs = {'course': {'required': True}, 'mentor': {'required': True}, 'create_by': {'read_only': True}}

    def validate(self, data):
        data['create_by'] = self.context['user']
        return data


class StudentCourseMentorReadSerializer(serializers.ModelSerializer):
    """
        This Serializer is used for StudentCourseMentor Data Serializing Purpose
    """
    student = serializers.StringRelatedField(read_only=True)
    mentor = serializers.StringRelatedField(read_only=True)
    course = serializers.StringRelatedField(read_only=True)
    create_by = serializers.StringRelatedField(read_only=True)
    updated_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = StudentCourseMentor
        fields = "__all__"


class StudentCourseMentorUpdateSerializer(serializers.ModelSerializer):
    """
        This Serializer is used for StudentCourseMentorUpdate Data Serializing Purpose
    """
    class Meta:
        model = StudentCourseMentor
        fields = ['course', 'mentor', 'updated_by']
        extra_kwargs = {'course': {'required': True}, 'mentor': {'required': True}, 'updated_by': {'read_only': True}}

    def validate(self, data):
        data['updated_by'] = self.context['user']
        return data