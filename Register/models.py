from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    mobile_number = models.CharField(max_length=13, default=None, null=True, unique=True)
    role = models.CharField(
        choices=(
            ('Mentor', 'Mentor'),
            ('Student', 'Student'),
            ('Admin', 'Admin')
        ), max_length=20)
    is_first_time_login = models.BooleanField(default=True)

    def get_user_name(self):
        return self.username
