from rest_framework import permissions

SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']


class Admin_validate(permissions.BasePermission):
    """
        This class is used to give permission to Admin user only
    """
    def has_permission(self, request, view):
        return request.user.role == 'Admin'


class Mentor_validate(permissions.BasePermission):
    """
        This class is used to give permission to Admin/Mentor user only
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user.role == 'Mentor' or request.user.role == 'Admin'
        else:
            return request.user.role == 'Mentor'


class Student_validate(permissions.BasePermission):
    """
        This class is used to give permission to Admin/Mentor/Student users
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user.role == 'Admin' or request.user.role == 'Mentor' or request.user.role == 'Student'
        else:
            return request.user.role == 'Student'


