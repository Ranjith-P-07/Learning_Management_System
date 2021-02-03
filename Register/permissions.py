from rest_framework import permissions


class Admin_validate(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.role == 'Admin':
            return True
        return False


class Mentor_validate(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.role == 'Mentor':
            return True
        return False


class Student_validate(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.role == 'Student':
            return True
        return False
