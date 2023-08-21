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


class TestSearchView(TestCase):
    
    def setUp(self):
        self.category = Category.objects.create(name='Food')
        self.product = Product.objects.create(name='pepperoni', description="deliciouse", category=self.category, price=10)
        self.client = Client()

    def tearDown(self):
        Product.objects.all().delete()
        Category.objects.all().delete()
    
    def test_search_get_no_data(self):
        response = self.client.get(reverse('menu:search'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['message'], None)
        self.assertFalse(response.context['search_result'])
        self.assertTemplateUsed('menu/search.html')
        self.assertTemplateNotUsed('menu/menu.html')
        self.assertTemplateNotUsed('home/home.html')


    def test_search_get_invaid_serach_data(self):
        response = self.client.get(reverse('menu:search'), data={'search': '111111'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['message'], 'Nothing was found for 111111')
        self.assertFalse(response.context['search_result'])
        self.assertTemplateUsed('menu/search.html')
        self.assertTemplateNotUsed('menu/menu.html')
        self.assertTemplateNotUsed('home/home.html')


    def test_search_get_valid_serach_data(self):
        response = self.client.get(reverse('menu:search'), data={'search': 'pep'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['message'], None)
        self.assertIn(self.product, response.context['search_result'])
        self.assertTemplateUsed('menu/search.html')
        self.assertTemplateNotUsed('menu/menu.html')
        self.assertTemplateNotUsed('home/home.html')


