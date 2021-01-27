from django.db import models
import sys

sys.path.append('..')
from Register.models import User


class Course(models.Model):
    course_name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.course_name


class Mentor(models.Model):
    mentor = models.OneToOneField(User, on_delete=models.CASCADE)
    course = models.ManyToManyField(to=Course, blank=True)

    def __str__(self):
        return self.mentor.get_user_name()


class Student(models.Model):
    year_of_experience = (
        (0, 0),
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    )
    student = models.OneToOneField(User, on_delete=models.CASCADE)
    alternate_number = models.CharField(max_length=13, default=None, null=True, blank=True)
    Relationship_with_alternate_contact_person = models.CharField(max_length=50, default=None, null=True, blank=True)
    current_location = models.CharField(max_length=50, default=None, null=True, blank=True)
    current_address = models.CharField(max_length=50, default=None, null=True, blank=True)
    git_link = models.CharField(max_length=30, default=None, null=True, blank=True)
    year_of_experience = models.IntegerField(choices=year_of_experience, default=None, null=True)

    def __str__(self):
        return self.student.get_user_name()


class Education(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    institute = models.CharField(max_length=50, default=None, null=True, blank=True)
    degree = models.CharField(max_length=50, default=None, null=True, blank=True)
    stream = models.CharField(max_length=50, default=None, null=True, blank=True)
    percentage = models.FloatField(default=None, null=True, blank=True)
    from_date = models.DateField(default=None, blank=True, null=True)
    till = models.DateField(default=None, blank=True, null=True)

    def __str__(self):
        return self.student.student.get_user_name()


class Performance(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    mentor = models.ForeignKey(Mentor, on_delete=models.SET_NULL, null=True)
    assesment_day = models.CharField(max_length=10, default=None, blank=True, null=True)
    current_score = models.FloatField()

    def __str__(self):
        return self.student.get_user_name()
