from django.test import TestCase
from accounts.models import User

class TestCustomUser(TestCase):

    def test_str(self):
        user = User.objects.create_user(phone='09198470934', password='reza123456')
        self.assertEqual(str(user), '09198470934')