from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from .serializers import UserRegistrationSerializer, UserLoginSerializer
from django.contrib.auth import authenticate, login, logout
from .permissions import Admin_validate
from django.contrib.sites.shortcuts import get_current_site
import sys

sys.path.append('..')
from LMS.EmailConf import Email


class UserRegistrationView(GenericAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = (Admin_validate,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {
            'username': request.data['username'],
            'password': request.data['password'],
            'role': request.data['role'],
            'email': request.data['email'],
            'domain': get_current_site(request).domain
        }
        Email.sendEmail(Email.addingMailBody(data))
        return Response({
                            'response': f"Hello {request.data['username']} you were added as a {request.data['role']},Check your mail for verification"},
                        status=status.HTTP_201_CREATED)


class UserLoginView(GenericAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.data.get('username')
        password = serializer.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return Response({'response': 'You are successfully logged in'}, status=status.HTTP_200_OK)
        return Response({'response': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
