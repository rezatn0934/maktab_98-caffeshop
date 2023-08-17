from django.test import SimpleTestCase
from django.urls import reverse, resolve
from accounts import views


class TestUrls(SimpleTestCase):
    def test_login(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func.view_class, views.StaffLogin)

    def test_verify(self):
        url = reverse('verify')
        self.assertEqual(resolve(url).func.view_class, views.Verify)
