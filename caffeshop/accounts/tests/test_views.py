from django.test import TestCase, Client
from django.urls import reverse

from accounts.models import User
from accounts.form import CustomUserCreationForm
from accounts.views import (
    StaffLogin,
)


class TestStaffLogin(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(
            phone='09038916990',
            password='reza123456',
            first_name='reza',
            last_name='teymouri'
        )

    def test_staff_login_GET(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        self.failUnless(response.context['form'], CustomUserCreationForm)
