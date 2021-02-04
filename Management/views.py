from django.utils.decorators import method_decorator
from rest_framework.generics import GenericAPIView
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import CourseSerializer, MentorSerializer, MentorUpdateSerializer, StudentSerializer, \
    StudentCourseMentorSerializer, \
    StudentCourseMentorReadSerializer, StudentEducationSerializer, StudentCourseMentorUpdateSerializer
from .models import Course, Mentor, Student, Education, StudentCourseMentor
from django.contrib.auth.decorators import login_required

import logging
from LMS.settings import file_handler

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)

import sys

sys.path.append('..')
from Register.permissions import Admin_validate, Mentor_validate, Student_validate


@method_decorator(login_required(login_url='/user/login/'), name='dispatch')
class CoursesAPIView(generics.ListCreateAPIView):
    serializer_class = CourseSerializer
    permission_classes = (Admin_validate,)

    def get_queryset(self):
        """
            Returns a list of all create courses
        """
        queryset = Course.objects.all()
        logger.info("Listed all courses, from get()")
        return queryset

    def perform_create(self, serializer):
        """
            create a new course instance
        """
        serializer.save()
        logger.info("New course is created, from create()")
        return Response({'response': 'Course is successfully added'}, status=status.HTTP_201_CREATED)


@method_decorator(login_required(login_url='/user/login/'), name='dispatch')
class CourseUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CourseSerializer
    permission_classes = (Admin_validate,)
    queryset = Course.objects.all()
    lookup_field = 'id'

    def perform_update(self, serializer):
        """
            Updating a course instance
        """
        serializer.save()
        logger.info("Course is Updated")
        return Response({'response': 'Course is updated'}, status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        """
            Deleting a course instance
        """
        instance.delete()
        logger.info("Course is Deleted")
        return Response({'response': 'Course is deleted'}, status=status.HTTP_204_NO_CONTENT)


@method_decorator(login_required(login_url='/user/login/'), name='dispatch')
class MentorAPIView(generics.ListAPIView):
    """
        Listing all mentor objects
    """
    serializer_class = MentorSerializer
    permission_classes = (Admin_validate,)

    queryset = Mentor.objects.all()


@method_decorator(login_required(login_url='/user/login/'), name='dispatch')
class MentorUpdateAPIView(GenericAPIView):
    serializer_class = MentorUpdateSerializer
    permission_classes = (Admin_validate,)
    queryset = Mentor.objects.all()

    def get(self, request, id):
        """"
            Getting particular mentor based on id
        """
        try:
            mentor = self.queryset.get(id=id)
            serializer = MentorSerializer(mentor)
            logger.info("Particular mentor is obtained")
            return Response({'response': serializer.data}, status=status.HTTP_200_OK)
        except:
            logger.error("Mentor not found")
            return Response({'response': 'Mentor not found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, id):
        """
            Updating particular mentor by id
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            mentor = self.queryset.get(id=id)
            for course_id in serializer.data.get('course'):
                for mentor_course in mentor.course.all():
                    if course_id == mentor_course.id:
                        logger.error("This course is already added")
                        return Response({'response': 'This course is already added'},
                                        status=status.HTTP_400_BAD_REQUEST)
                mentor.course.add(course_id)
            logger.info("New course is added for the mentor")
            return Response({'response': f" New course is/are added to {mentor}'s course list"})
        except Mentor.DoesNotExist:
            logger.error("Mentor id does not exist")
            return Response({'response': 'Mentor id does not exist'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        try:
            mentor = self.queryset.get(id=id)
            mentor.delete()
            return Response({'response': 'Mentor is deleted successfully!!'}, status=status.HTTP_200_OK)
        except:
            return Response({'response': 'Mentor not found'}, status=status.HTTP_404_NOT_FOUND)


@method_decorator(login_required(login_url='/user/login/'), name='dispatch')
class StudentPersonalDetailAPIView(GenericAPIView):
    """
        This API is used to Enter Personal Details of Student
    """
    serializer_class = StudentSerializer
    permission_classes = (Student_validate,)
    queryset = Student.objects.all()

    def put(self, request, id):
        """
            This method is used to update Student Personal data
        """
        try:
            instance = self.queryset.get(id=id)
            serializer = self.serializer_class(instance, data=request.data)
            if serializer.is_valid():
                serializer.save(id=id)
                logger.info("Student Personal data is Updated succesfully")
                return Response({'details': 'Student Personal data is Updated succesfully'}, status=status.HTTP_200_OK)
            logger.error("Student Personal data is not updated")
            return Response({'response': 'Student Personal data is not updated'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'response': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)


@method_decorator(login_required(login_url='/user/login/'), name='dispatch')
class StudentEducationAPIView(GenericAPIView):
    """
        This API is used to add Education Details of Student
    """
    serializer_class = StudentEducationSerializer
    permission_classes = (Student_validate,)
    queryset = Education.objects.all()

    def get(self, request, id):
        """
            This method is used to get Student Education Details
        """
        try:
            student = self.queryset.filter(id=id)
            if student:
                serializer = self.serializer_class(student, many=True)
                logger.info("Obtained student Details")
                return Response({'response': serializer.data}, status=status.HTTP_200_OK)
            return Response({'response': 'Student not found'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            logger.error("Student not Found")
            return Response({'response': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, id):

        try:
            instance = self.queryset.get(id=id)
            serializer = self.serializer_class(instance, data=request.data)
            if serializer.is_valid():
                serializer.save()
                logger.info("Student Education data is Updated succesfully")
                return Response({'details': 'Student Education data is Updated succesfully'}, status=status.HTTP_200_OK)
            logger.error("Student Education data is not updated")
            return Response({'response': 'Student Education data is not updated'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            logger.error("Student Education details not Found")
            return Response({'response': 'Student Education details not Found'}, status=status.HTTP_404_NOT_FOUND)


@method_decorator(login_required(login_url='/user/login/'), name='dispatch')
class StudentCourseMentorMapAPIView(GenericAPIView):
    serializer_class = StudentCourseMentorSerializer
    permission_classes = (Admin_validate,)
    queryset = StudentCourseMentor.objects.all()

    def get(self, request):
        """
            This API is used to get student course mentor mapped records
        """
        serializer = StudentCourseMentorReadSerializer(self.queryset.all(), many=True)
        if not serializer.data:
            logger.info('Records not found')
            return Response({'response': 'Records not found'}, status=status.HTTP_404_NOT_FOUND)
        logger.info('student course mentor mapped records fetched')
        return Response({'response': serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        """
            This API is used to post student course mentor mapped record
        """
        serializer = self.serializer_class(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        mentor = serializer.validated_data.get('mentor')
        course = serializer.validated_data.get('course')
        if mentor is None or course is None:
            return Response({'response': "Mentor or Course can not be Null"}, status=status.HTTP_400_BAD_REQUEST)
        if course in mentor.course.all():
            serializer.save()
            logger.info('Record added')
            return Response({'response': "Record added"}, status=status.HTTP_200_OK)
        logger.info('course not in mentor bucket')
        return Response({'response:': f"{course.course_name} is not in {mentor.mentor.get_full_name()}''s Course list"}
                        , status=status.HTTP_404_NOT_FOUND)


@method_decorator(login_required(login_url='/user/login/'), name='dispatch')
class StudentCourseMentorUpdateAPIView(GenericAPIView):
    serializer_class = StudentCourseMentorUpdateSerializer
    permission_classes = (Admin_validate,)
    queryset = StudentCourseMentor.objects.all()

    def put(self, request, id):
        """
            This API is used to update student course mentor mapping
           @param request: Course id and mentor id
           @param record_id: record id of StudentCourseMentor model
           @return: updates record
        """
        try:
            instance = self.queryset.get(id=id)
            serializer = self.serializer_class(instance, data=request.data, context={'user': request.user})
            serializer.is_valid(raise_exception=True)
            mentor = serializer.validated_data.get('mentor')
            course = serializer.validated_data.get('course')
            if mentor is None or course is None:
                return Response({'response': "Mentor or Course can not be Null"}, status=status.HTTP_400_BAD_REQUEST)
            if course in mentor.course.all():
                serializer.save()
                return Response({'response': "Record Updated"}, status=status.HTTP_200_OK)
        except:
            return Response({'response:': f"{course.course_name} is not in {mentor.mentor.get_full_name()}''s Course list"}
                        , status=status.HTTP_404_NOT_FOUND)
