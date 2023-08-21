from django.test import TestCase
from accounts.models import User
from accounts.authentication import PhoneAuthBackend


class TestAuthentication(TestCase):

    def setUp(self):
        self.user = User.objects.create(phone="09117200513", password="Ffarzam_1992")

    def tearDown(self):
        self.user.delete()

    def test_get_user(self):
        user_check = PhoneAuthBackend().get_user(self.user.id)
        self.assertEqual(self.user.phone, user_check.phone)

    def test_get_user_fail(self):

        user = PhoneAuthBackend().get_user(10)
        self.assertIsNone(user)