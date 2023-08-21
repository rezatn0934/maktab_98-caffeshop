from django.test import SimpleTestCase
from django.urls import reverse, resolve
from menu.views import Menu, ProductView, search_product_view


class TestUrls(SimpleTestCase):

    def test_menu_url(self):
        url = reverse("menu:menu")
        self.assertEqual(resolve(url).func.view_class, Menu)


    def test_show_product_url(self):
        url = reverse("menu:show_product", args=(1,))
        self.assertEqual(resolve(url).func.view_class, ProductView)


