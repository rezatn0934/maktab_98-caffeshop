from django.test import TestCase, Client
from django.urls import reverse
from menu.models import Product, Category
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings


class TestMenuView(TestCase):

    def setUp(self):
        self.client = Client()
        self.image = open(settings.MEDIA_ROOT / "images/test/pina_colada.png", 'rb').read()
        self.category = Category.objects.create(name='Food')
        self.product = Product.objects.create(name='pepperoni', category=self.category, price=100,
                                              image=SimpleUploadedFile.from_dict(
                                                  {'filename': 'product_pic.png', 'content': self.image,
                                                   'content_tye': 'image/png'})
                                              )

    def tearDown(self):
        self.product.delete()
        self.category.delete()

    def test_menu_get(self):
        response = self.client.get(reverse('menu:menu'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('menu/menu.html')
        self.assertTemplateNotUsed('menu/search.html')
        self.assertTemplateNotUsed('home/home.html')

    def test_menu_search_valid(self):
        headers = {'HTTP_HX-Request': 'true'}
        response = self.client.get(reverse('menu:menu'), data={'search': 'pep'}, **headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.product.name, response.context['items'][0].name)
        self.assertTemplateUsed('menu/search_results.html')

    def test_menu_search_not_valid(self):
        headers = {'HTTP_HX-Request': 'true'}
        response = self.client.get(reverse('menu:menu'), data={'search': '111111'}, **headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['items'], ['Nothing Was Found'])
        self.assertTemplateUsed('menu/search_results.html')
        self.assertTemplateNotUsed('menu/search.html')

# class TestSearchView(TestCase):
#
#     def setUp(self):
#         self.image = open(settings.MEDIA_ROOT / "images/test/pina_colada.png", 'rb').read()
#         self.category = Category.objects.create(name='Food')
#         self.product = Product.objects.create(name='pepperoni', category=self.category, price=100,
#                                               image=SimpleUploadedFile.from_dict(
#                                                   {'filename': 'product_pic.png', 'content': self.image,
#                                                    'content_tye': 'image/png'})
#                                               )
#         self.client = Client()
#
#     def tearDown(self):
#         self.product.delete()
#         self.category.delete()
#
#     def test_search_get_no_data(self):
#         response = self.client.get(reverse('menu:search'))
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.context['items'], [])
#         self.assertTemplateUsed('menu/search.html')
#
#     def test_search_get_invalid_search_data(self):
#         response = self.client.get(reverse('menu:search'), data={'search': '111111'})
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.context['items'], ['Nothing Was Found'])
#         self.assertTemplateUsed('menu/search_results.html')
#         self.assertTemplateNotUsed('menu/search.html')
#
#     def test_search_get_valid_search_data(self):
#         response = self.client.get(reverse('menu:search'), data={'search': 'pep'})
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(self.product.name, response.context['items'][0].name)
#         self.assertTemplateUsed('menu/search_results.html')