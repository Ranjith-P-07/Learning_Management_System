from rest_framework import permissions


class Admin_validate(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'Admin'


class Mentor_validate(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'Mentor'


class IsMentorAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'Mentor' or request.user.role == 'Admin'


class Student_validate(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'Student'

