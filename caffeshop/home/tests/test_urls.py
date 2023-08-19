from django.test import SimpleTestCase
from django.urls import reverse, resolve
from home.views import HomeView


class TestUrls(SimpleTestCase):

    def test_home(self):
        url = reverse("home")
        self.assertEqual(resolve(url).func.view_class, HomeView)
