from django.test import TestCase
from accounts.models import User


class TestManager(TestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(phone="09117200513", password="Ffarzam_1992")

    def tearDown(self):
        self.superuser.delete()

    def test_create_user(self):
        with self.assertRaises(ValueError):
            user = User.objects.create_user(phone=None, password="Ffarzam_1992")

    def test_create_superuser(self):
        superuser_check = User.objects.get()
        self.assertEqual(self.superuser, superuser_check)

