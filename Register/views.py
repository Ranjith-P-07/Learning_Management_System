from .models import User
from django.core.validators import validate_email
from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from .serializers import UserRegistrationSerializer, UserLoginSerializer, EmailSerializers, ResetSerializers, \
    ChangeUserPasswordSerializer
from django.contrib.auth import authenticate, login, logout
from .permissions import Admin_validate
from django.contrib.sites.shortcuts import get_current_site
from .token import token_activation
from django_short_url.views import get_surl
from django_short_url.models import ShortURL
import jwt
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from LMS import settings

import logging
from LMS.settings import file_handler

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)

import sys

sys.path.append('..')
from LMS.EmailConf import Email

from django.contrib.auth.hashers import check_password


@method_decorator(login_required(login_url='/user/login/'), name='dispatch')
class UserRegistrationView(GenericAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = (Admin_validate,)

    def post(self, request):
        """
        This API is used to Add user like Mentor,Engineer or another Admin to the system by an Admin
        and informs the user about their account creation via email
        request parms : user related data like username, name, email etc
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        token = token_activation(username=request.data['username'], password=request.data['password'])
        url = str(token)
        surl = get_surl(url)
        short_token = surl.split('/')
        data = {
            'username': request.data['username'],
            'password': request.data['password'],
            'role': request.data['role'],
            'email': request.data['email'],
            'domain': get_current_site(request).domain,
            'token': short_token[2],
        }
        Email.sendEmail(Email.addingMailBodyForRegister(data))
        logger.info("Email has been sent..!!, from post()")
        return Response({
            'response': f"Hello {request.data['username']} you were added as a {request.data['role']},Check your mail for verification"},
            status=status.HTTP_201_CREATED)


class UserLoginView(GenericAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request):
        """
        This API is Used for user login
        request parms: username, Password
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.data.get('username')
        password = serializer.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            if user.is_first_time_login:
                login(request, user)
                return Response(
                    {'response': 'You are logged in! Now you need to change password by using token to access other Functions'},
                    status=status.HTTP_200_OK)
            login(request, user)
            logger.info("Logged in successfully, from post()")
            return Response({'response': 'You are successfully logged in'}, status=status.HTTP_200_OK)
        logger.error("Invalid Credentials, from post()")
        return Response({'response': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@method_decorator(login_required(login_url='/user/login/'), name='dispatch')
class UserLogoutView(GenericAPIView):
    """
        This api is for user log out
        @return: release all resources from user on logged out
    """
    serializer_class = UserLoginSerializer

    def get(self, request):
        try:
            logout(request)
            logger.info('your succefully logged out,thankyou')
            return Response({'details': 'your succefully logged out,thankyou'}, status=status.HTTP_200_OK)
        except Exception:
            logger.error('something went wrong while logout')
            return Response({'details': 'something went wrong while logout'}, status=status.HTTP_403_FORBIDDEN)


@method_decorator(login_required(login_url='/user/login/'), name='dispatch')
class ChangePasswordForFirstAccess(GenericAPIView):
    serializer_class = ChangeUserPasswordSerializer

    def put(self, request, surl):
        """This API is used to change user password
        @request_parms = old password, new password and confirm password
        @rtype: saves new password in database
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_data = request.user
        user = User.objects.get(id=user_data.id)
        username = request.user.username
        tokenobject = ShortURL.objects.get(surl=surl)
        token = tokenobject.lurl
        decoded = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
        decoded_username = decoded['username']
        if username == decoded_username:
            old_password = serializer.data.get('old_password')
            if check_password(old_password, request.user.password):
                user.set_password(raw_password=serializer.data.get('new_password'))
                user.is_first_time_login = False
                user.save()
                return Response({'response': 'Your password is changed successfully!, Now You can access your Resources'}, status=status.HTTP_200_OK)
            return Response({'response': 'Old password does not match!'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({'response': 'Invalid token..!!'}, status=status.HTTP_401_UNAUTHORIZED)


class ForgotPasswordView(GenericAPIView):
    serializer_class = EmailSerializers

    def post(self, request):

        email = request.data['email']
        if email == "":
            logger.error('email should not be empty')
            return Response({'details': 'email should not be empty'})
        else:
            try:
                validate_email(email)
            except Exception:
                logger.error('not a valid email')
                return Response({'response_msg': 'not a valid email'}, status=status.HTTP_400_BAD_REQUEST)
            try:
                user = User.objects.get(email=email)
                if user:
                    token = token_activation(username=user.username, password=user.password)
                    url = str(token)
                    surl = get_surl(url)
                    short_token = surl.split('/')
                    data = {
                        'username': user,
                        'domain': get_current_site(request).domain,
                        'surl': short_token[2]
                    }
                    Email.sendEmail(Email.addingMailBodyForForgot(data))
                    logger.info('please check your email,link has sent your email, from forgotpassword')
                    return Response({'details': 'please check your email,link has sent your email'},
                                    status=status.HTTP_200_OK)
            except User.DoesNotExist:
                logger.error('something went wrong')
                return Response({'response_msg':'User DoesnotExist'}, status=status.HTTP_404_NOT_FOUND)


class ResetPassword(GenericAPIView):
    serializer_class = ResetSerializers

    def post(self, request, surl):
        """
            This API is used to reset user password
            @param: user id and decoded token fetched for resetpassword request
            @return: reset user password
        """
        password1 = request.data['password']
        try:
            tokenobject = ShortURL.objects.get(surl=surl)
            token = tokenobject.lurl
            decoded = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
            username = decoded['username']
            user = User.objects.get(username=username)
            user_reset = str(user)

            if user_reset is None:
                logger.error('not a valid user')
                return Response({'details': 'not a valid user'})
            elif (password1) == "":
                logger.error('password should not be empty')
                return Response({'details': 'password should not be empty'})
            else:
                try:
                    user = User.objects.get(username=user_reset)
                    user.set_password(password1)
                    user.save()
                    logger.info('your password has been Set')
                    return Response({'details': 'your password has been Set'})
                except Exception:
                    logger.error('not a valid user')
                    return Response({'details': 'not a valid user'})
        except Exception:
            return Response({'response': "Invalid token"})


@method_decorator(login_required(login_url='/user/login/'), name='dispatch')
class ChangePassword(GenericAPIView):
    serializer_class = ChangeUserPasswordSerializer

    def put(self, request):
        """This API is used to change user password
        @request_parms = old password, new password and confirm password
        @rtype: saves new password in database
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_data = request.user
        user = User.objects.get(id=user_data.id)
        old_password = serializer.data.get('old_password')
        if check_password(old_password, request.user.password):
            user.set_password(raw_password=serializer.data.get('new_password'))
            user.is_first_time_login = False
            user.save()
            return Response({'response': 'Your password is changed successfully!'}, status=status.HTTP_200_OK)
        return Response({'response': 'Old password does not match!'}, status=status.HTTP_401_UNAUTHORIZED)