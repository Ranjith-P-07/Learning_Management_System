from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('forgotpassword/', views.ForgotPasswordView.as_view(), name='forgotpassword'),
    path('resetpassword/<surl>/', views.ResetPassword.as_view(), name="resetpassword"),
    path('change_password/<surl>/', views.ChangePasswordForFirstAccess.as_view(), name='change_password'),
    path('changepassword/', views.ChangePassword.as_view(), name='changepassword'),
]