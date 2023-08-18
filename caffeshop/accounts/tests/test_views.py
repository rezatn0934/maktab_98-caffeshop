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

    def test_staff_login_POST_valid(self):
        response = self.client.post(reverse('login'), data={'phone': '09038916990'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('verify'))

    def test_staff_login_POST_invalid(self):
        response = self.client.post(reverse('login'), data={'phone': 'gfhbjnh'})
        self.assertEqual(response.status_code, 200)
        self.failIf(response.context['form'].is_valid())
        self.assertEqual(response.context['message'], 'Wrong input, Phone number Should Start 11 digits Like 09*********')
        self.assertFormError(form=response.context['form'], field='phone', errors='Enter a valid value.')
