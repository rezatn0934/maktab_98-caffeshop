from django.test import TestCase, Client
from django.urls import reverse, resolve
from menu.views import Menu, ProductView, search_product_view
from menu.models import Product, Category
from model_bakery import baker
from django.utils.html import mark_safe



class TestMenuView(TestCase):
    
    def setUp(self):
        self.client = Client()
    
    def test_menu_get(self):
        response = self.client.get(reverse('menu:menu'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('menu/menu.html')
        self.assertTemplateNotUsed('menu/search.html')
        self.assertTemplateNotUsed('home/home.html')

