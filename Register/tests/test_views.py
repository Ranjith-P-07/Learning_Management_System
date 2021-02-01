from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from ..models import User
import json

CONTENT_TYPE = 'application/json'


class AuthenticationAPITest(TestCase):
    """ Test module for authentication APIs """

    def setUp(self):
        # initialize the APIClient app
        self.client = Client()
        user1 = User.objects.create(username='Ranjith', email='ranjithroy705@gmail.com',
                                    password='pbkdf2_sha256$216000$0gRtmSAKA8eg$LDXyQf0Tm5gnznV6IadBVqE6KURr90Xd1wq0drhlq0g=',
                                    is_superuser=True, role='Admin')

        self.valid_payload_user1 = {
            'username': 'Ranjith',
            'password': '7353469961',
        }

        self.invalid_credentials = {
            'username': 'Ranju12',
            'password': '123',
        }

        self.valid_payload = {
            "username": "string",
            "first_name": "string",
            "last_name": "string",
            "email": "user@example.com",
            "mobile_number": "string",
            "role": "Mentor",
            "password": "string",
            "confirm_password": "string"
        }

        self.invalid_payload = {
            "username": "string",
            "mobile_number": "string",
            "password": "string",
            "confirm_password": "string"
        }

    def test_register_user_with_valid_payload_without_login(self):
        response = self.client.post(reverse('register'), data=json.dumps(self.valid_payload_user1),
                                    content_type='application/json', follow=True)
        self.assertEquals(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_register_user_with_valid_payload(self):
        self.client.post(reverse('login'), data=json.dumps(self.valid_payload_user1), content_type=CONTENT_TYPE)
        response = self.client.post(reverse('register'), data=json.dumps(self.valid_payload),
                                    content_type='application/json', follow=True)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    def test_register_user_with_invalid_payload(self):
        self.client.post(reverse('login'), data=json.dumps(self.valid_payload_user1), content_type=CONTENT_TYPE)
        response = self.client.post(reverse('register'), data=json.dumps(self.invalid_payload),
                                    content_type='application/json', follow=True)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_with_valid_credentials(self):
        response = self.client.post(reverse('login'), data=json.dumps(self.valid_payload_user1),
                                    content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_with_invalid_credentials(self):
        response = self.client.post(reverse('login'), data=json.dumps(self.invalid_credentials),
                                    content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout(self):
        self.client.post(reverse('login'), data=json.dumps(self.valid_payload_user1), content_type=CONTENT_TYPE)
        response = self.client.get(reverse('logout'), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout_with_invalid_credentials(self):
        self.client.post(reverse('login'), data=json.dumps(self.invalid_credentials), content_type=CONTENT_TYPE)
        response = self.client.get(reverse('logout'), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_logout_without_login(self):
        response = self.client.get(reverse('logout'), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_forgot_password_api_when_mail_id_is_registered(self):
        self.test_register_user_with_valid_payload()
        email = json.dumps({'email': 'user@example.com'})
        response = self.client.post(reverse('forgotpassword'), data=email, content_type='application/json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_forgot_password_api_when_mail_id_is_not_registered(self):
        email = json.dumps({'email': 'user12@example.com'})
        response = self.client.post(reverse('forgotpassword'), data=email, content_type='application/json')
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_forgot_password_api_when_mail_id_is_invalid(self):
        email = json.dumps({'email': 'user1123.com'})
        response = self.client.post(reverse('forgotpassword'), data=email, content_type='application/json')
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_change_password_api_with_valid_credentials(self):
        self.client.post(reverse('login'), data=json.dumps(self.valid_payload_user1), content_type=CONTENT_TYPE)
        data = json.dumps({
          "old_password": "7353469961",
          "new_password": "string",
          "confirm_password": "string"
        })
        response = self.client.put(reverse('changepassword'), data=data, content_type='application/json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_change_password_api_with_invalid_credentials(self):
        self.client.post(reverse('login'), data=json.dumps(self.valid_payload_user1), content_type=CONTENT_TYPE)
        data = json.dumps({
          "old_password": "vgdhdery",
          "new_password": "string",
          "confirm_password": "string"
        })
        response = self.client.put(reverse('changepassword'), data=data, content_type='application/json')
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)








