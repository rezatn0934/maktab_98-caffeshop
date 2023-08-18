from django.test import TestCase
from accounts.form import CustomUserCreationForm, CustomUserChangeForm
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

    def test_clean_username(self):
        User.objects.create_user(phone='09198470934', password='rtn093471')
        form = CustomUserCreationForm(
            data={'phone': '09198470934', 'first_name': 'reza', 'last_name': 'teymouri', 'password1': 'reza123456',
                  'password2': 'reza123456'})
        self.assertEqual(len(form.errors), 1)
        self.assertTrue(form.has_error)

    def test_unmatched_passwords(self):
        form = CustomUserCreationForm(
            data={'phone': '09198470934', 'first_name': 'reza', 'last_name': 'teymouri', 'password1': 'reza123456',
                  'password2': 'reza1234'})
        self.assertEqual(len(form.errors), 1)
        self.assertTrue(form.has_error)

    def test_wrong_phone_regex(self):
        form = CustomUserCreationForm(
            data={'phone': '9198470934', 'first_name': 'reza', 'last_name': 'teymouri', 'password1': 'reza123456',
                  'password2': 'reza123456'})
        self.assertEqual(len(form.errors), 1)
        self.assertTrue(form.has_error)


class TestUseChangeForm(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            phone='09038916990',
            password='reza123456',
            first_name='reza',
            last_name='teymouri'
        )
    def test_valid_data(self):
        form = CustomUserChangeForm(data={'phone': '0903891990', 'first_name': 'ali', 'last_name': 'ahmadi'})
        self.assertTrue(form.is_valid)

    def test_empty_form(self):
        form = CustomUserChangeForm()
        self.assertFalse(form.is_valid())
