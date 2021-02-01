from django.test import TestCase
from ..models import User


class UserRegistrationTest(TestCase):
    """ Test module for Registration model """
    def setUp(self):
        User.objects.create(
            username='Ranjith', email='ranjith@gmail.com', password='123456r', mobile_number='9076543214')
        User.objects.create(
            username='Rahul', email='rahul@gmail.com', password='123456', mobile_number='9054324567')

    def test_registeration_username(self):
        registration_Ranjith = User.objects.get(username='Ranjith')
        registration_Rahul = User.objects.get(username='Rahul')
        self.assertEqual(registration_Ranjith.get_username(), "Ranjith")
        self.assertEqual(registration_Rahul.get_username(), "Rahul")

    def test_registeration_mobile_number(self):
        registration_Ranjith_mobile_number = User.objects.get(username='Ranjith')
        registration_Rahul_mobile_number = User.objects.get(username='Rahul')
        self.assertEqual(registration_Ranjith_mobile_number.get_mobile_number(), '9076543214')
        self.assertEqual(registration_Rahul_mobile_number.get_mobile_number(), '9054324567')

    def test_registeration_email(self):
        registration_Ranjith_mobile_number = User.objects.get(username='Ranjith')
        registration_Rahul_mobile_number = User.objects.get(username='Rahul')
        self.assertEqual(registration_Ranjith_mobile_number.get_email(), 'ranjith@gmail.com')
        self.assertEqual(registration_Rahul_mobile_number.get_email(), 'rahul@gmail.com')