from ..models import User
from ..serializers import UserRegistrationSerializer, UserLoginSerializer, EmailSerializers, ResetSerializers, \
    ChangeUserPasswordSerializer
from django.test import TestCase


class TestSerializer(TestCase):
    def setUp(self):
        """
        This is setup for testing serializers
        """
        # User Attributes
        self.user_attributes = {
            'username': 'Ranjith',
            'first_name': 'Ranjith',
            'last_name': 'ranju',
            'email': 'ranjith@gmail.com',
            'mobile_number': '9035678754',
            'role': 'Student',
            'password': '123456',
        }

        self.user1_attributes = {
            'username': 'Ranjith',
            'first_name': 'Ranjith',
            'last_name': 'ranju',
            'email': 'ranjith@gmail.com',
            'mobile_number': '9035678754',
            'role': 'Student',
            'password': '123456',
            'confirm_password': '123456',
        }

        # User Login serializer attributes
        self.login_attributes = {
            'username': 'Ranjith',
            'password': '123456'
        }
        # User Forgot Password serializer attributes
        self.forgot_attributes = {
            'email': 'ranjith@gmail.com'
        }
        # User change password serializer attributes
        self.change_password_attributes = {
            'old_password': '123456',
            'new_password': '12345',
            'confirm_password': '12345'
        }
        # User reset password serializer attributes
        self.reset_password_attributes = {
            'password': '123456',
        }

        self.user = User.objects.create(**self.user_attributes)
        self.user_serializer = UserRegistrationSerializer(instance=self.user1_attributes)
        self.forgot_serializer = EmailSerializers(instance=self.user)
        self.login_serializer = UserLoginSerializer(instance=self.login_attributes)
        self.change_password_serializer = ChangeUserPasswordSerializer(instance=self.change_password_attributes)
        self.reset_password_serializer = ResetSerializers(instance=self.user)

        # Test cases for user serializer

    def test_User_Serializers_Contains_Expected_Fields(self):
        """ This test case test the user registration serializer contains expected fields """
        data = self.user_serializer.data
        self.assertEqual(set(data.keys()),
                         {'username', 'first_name', 'last_name', 'email', 'mobile_number', 'role', 'password',
                          'confirm_password'})

    def test_User_Serializer_Username_Field(self):
        """ This test case test the user serializer fields"""
        data = self.user_serializer.data
        self.assertEqual(data['username'], self.user_attributes['username'])

    def test_User_Serializer_Username_Fields_Null_Content(self):
        """ This test case test the username field contains null content"""
        self.user_attributes['username'] = ''
        serializer = UserRegistrationSerializer(data=self.user_attributes)
        self.assertFalse(serializer.is_valid())

    def test_User_Serializer_Username_Field_Valid_Content(self):
        """ This test case test the username field contains valid content"""
        self.user1_attributes['username'] = 'Ranjith'
        serializer = UserRegistrationSerializer(data=self.user1_attributes)
        serializer.is_valid()
        self.assertEqual(serializer.data['username'], self.user1_attributes['username'])

    # Test cases for forgot password(Email) serializer
    def test_Forgot_Password_Serializers_Fields(self):
        data = self.forgot_serializer.data
        self.assertEqual(set(data.keys()), {'email'})

    def test_Forgot_Password_Serializer_Email_Field(self):
        data = self.forgot_serializer.data
        self.assertEqual(data['email'], self.forgot_attributes['email'])

    def test_Forgot_Password_Serializer_Email_Field_Invalid_Content(self):
        self.forgot_attributes['email'] = 'Ranjith'
        serializer = EmailSerializers(data=self.forgot_attributes)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), {'email'})

    def test_Forgot_Password_Serializer_Email_Field_Valid_Content(self):
        self.forgot_attributes['email'] = 'ranjith@gmail.com'
        serializer = EmailSerializers(data=self.forgot_attributes)
        self.assertTrue(serializer.is_valid())

    # test cases for login serializer
    def test_Login_Serializer_Contains_Expected_Fields(self):
        data = self.login_serializer.data
        self.assertEqual(set(data.keys()), {'username', 'password'})

    def test_Login_Serializer_Username_Field(self):
        data = self.login_serializer.data
        self.assertEqual(data['username'], self.login_attributes['username'])

    def test_Login_Serializer_Username_Fields_Content_Null(self):
        self.login_attributes['username'] = ''
        serializer = UserLoginSerializer(data=self.login_attributes)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), {'username'})

    def test_Login_Serializer_Username_Fields_Content_Min_length(self):
        self.login_attributes['username'] = 'a'
        serializer = UserLoginSerializer(data=self.login_attributes)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), {'username'})

    def test_Login_Serializer_Username_Fields_Content_Max_length(self):
        self.login_attributes['username'] = 'abhjkiolhjfdssfdgfdgttgthgth'
        serializer = UserLoginSerializer(data=self.login_attributes)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), {'username'})

    def test_Login_Serializer_password_Fields_Content_Null(self):
        self.login_attributes['password'] = ''
        serializer = UserLoginSerializer(data=self.login_attributes)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), {'password'})

    def test_Login_Serializer_Password_Fields_Content_Min_length(self):
        self.login_attributes['password'] = 'a'
        serializer = UserLoginSerializer(data=self.login_attributes)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), {'password'})

    def test_Login_Serializer_Password_Fields_Content_Max_length(self):
        self.login_attributes['password'] = 'abhjkiolhjfdssasdfghjklou'
        serializer = UserLoginSerializer(data=self.login_attributes)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), {'password'})

    def test_Login_Serializer_password_Fields_Valid_Content(self):
        self.login_attributes['password'] = '123456'
        serializer = UserLoginSerializer(data=self.login_attributes)
        self.assertTrue(serializer.is_valid())

    def test_Login_Serializer_Username_Fields_Valid_Content(self):
        self.login_attributes['username'] = 'Ranjith'
        serializer = UserLoginSerializer(data=self.login_attributes)
        self.assertTrue(serializer.is_valid())

    # test cases for change password serializer
    def test_Change_Password_Serializer_Contains_Expected_Fields(self):
        data = self.change_password_serializer.data
        self.assertEqual(set(data.keys()), {'old_password', 'new_password', 'confirm_password'})

    def test_Change_Password_Serializer_Username_Field(self):
        data = self.change_password_serializer.data
        self.assertEqual(data['new_password'], self.change_password_attributes['new_password'])

    def test_Change_Password_Serializer_Username_Fields_Content_Null(self):
        self.change_password_attributes['new_password'] = ''
        serializer = ChangeUserPasswordSerializer(data=self.change_password_attributes)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), {'new_password'})

    def test_Change_Password_Serializer_Username_Fields_Content_Min_length(self):
        self.change_password_attributes['new_password'] = 'a'
        serializer = ChangeUserPasswordSerializer(data=self.change_password_attributes)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), {'new_password'})

    def test_Change_Password_Serializer_Username_Fields_Content_Max_length(self):
        self.change_password_attributes['new_password'] = 'abhjkiolhjfdssdfgdg'
        serializer = ChangeUserPasswordSerializer(data=self.change_password_attributes)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), {'new_password'})

    def test_Change_Password_Serializer_Username_Fields_Valid_Content(self):
        self.change_password_attributes['new_password'] = '12345'
        serializer = ChangeUserPasswordSerializer(data=self.change_password_attributes)
        self.assertTrue(serializer.is_valid())

    # test cases for reset password serializer
    def test_Reset_Password_Serializer_Contains_Expected_Fields(self):
        """ This test case test the reset password serializer contains expected fields"""
        data = self.reset_password_serializer.data
        self.assertEqual(set(data.keys()), {'password'})

    def test_Reset_Password_Serializer_Username_Field(self):
        """ This test case test the reset password serializer fields"""
        data = self.reset_password_serializer.data
        self.assertEqual(data['password'], self.reset_password_attributes['password'])

    def test_Reset_Password_Serializer_New_Password_Fields_Null_Content(self):
        """ This test case test the password field contains null content"""
        self.reset_password_attributes['password'] = ''
        serializer = ResetSerializers(data=self.reset_password_attributes)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), {'password'})

    def test_Reset_Password_Serializer_New_Password_Fields_Min_length_Content(self):
        """ This test case test the password field contains minimum length content"""
        self.reset_password_attributes['password'] = 'a'
        serializer = ResetSerializers(data=self.reset_password_attributes)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), {'password'})

    def test_Reset_Password_Serializer_New_Password_Fields_Max_length_Content(self):
        """ This test case test the password field contains maximum length content"""
        self.reset_password_attributes['password'] = 'abhjkiolhjfdssdfgdg12345'
        serializer = ResetSerializers(data=self.reset_password_attributes)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), {'password'})

    def test_Reset_Password_Serializer_New_Password_Fields_Valid_Content(self):
        """ This test case test the password field contains valid content"""
        self.reset_password_attributes['password'] = '12345'
        serializer = ResetSerializers(data=self.reset_password_attributes)
        self.assertTrue(serializer.is_valid())

