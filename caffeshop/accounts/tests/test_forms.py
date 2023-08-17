from django.test import TestCase
from accounts.form import CustomUserCreationForm
from accounts.models import User


class TestUserCreationForm(TestCase):
    def test_valid_data(self):
        form = CustomUserCreationForm(
            data={'phone': '09198470934', 'first_name': 'reza', 'last_name': 'teymouri', 'password1': 'reza123456',
                  'password2': 'reza123456'})
        self.assertTrue(form.is_valid())

    def test_empty_form(self):
        form = CustomUserCreationForm()
        self.assertFalse(form.is_valid())
