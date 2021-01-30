from django.contrib import messages
from .models import User
from django.core.validators import validate_email
from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from .serializers import UserRegistrationSerializer, UserLoginSerializer, EmailSerializers, ResetSerializers
from django.contrib.auth import authenticate, login, logout
from .permissions import Admin_validate
from django.contrib.sites.shortcuts import get_current_site
from .token import token_activation
from django_short_url.views import get_surl
from django_short_url.models import ShortURL
import jwt
from LMS import settings
import sys

import logging
from LMS.settings import file_handler

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)

sys.path.append('..')
from LMS.EmailConf import Email


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
        data = {
            'username': request.data['username'],
            'password': request.data['password'],
            'role': request.data['role'],
            'email': request.data['email'],
            'domain': get_current_site(request).domain,
            # 'surl': short_token[2]
        }
        Email.sendEmail(Email.addingMailBodyForRegister(data))
        logger.info("Email has been sent..!!, from post()")
        return Response({
            'response': f"Hello {request.data['username']} you were added as a {request.data['role']},Check your mail for verification"},
            status=status.HTTP_201_CREATED)


# def changePassword(request, surl):
#     try:
#         tokenobject = ShortURL.objects.get(surl=surl)
#         token = tokenobject.lurl
#         decode = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
#         username = decode['username']
#         user = User.objects.get(username=username)
#         if user is not None:
#             user.is_active = True
#             user.save()
#             return redirect('login')
#         else:
#             return Response('not valid user')
#     except KeyError as e:
#         return Response(e)
#     except Exception as f:
#         return Response(f)


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
            login(request, user)
            logger.info("Logged in successfully, from post()")
            return Response({'response': 'You are successfully logged in'}, status=status.HTTP_200_OK)
        logger.error("Invalid Credentials, from post()")
        return Response({'response': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


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
                return Response({'details': 'not a valid email'})
            try:
                user = User.objects.get(email=email)
                print(user)
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
            except Exception as e:
                logger.error('something went wrong')
                return Response(e)


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
