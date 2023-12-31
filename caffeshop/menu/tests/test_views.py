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


class TestProductView(TestCase):

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

    def test_product_view_status_code(self):
        response = self.client.get(reverse('menu:show_product', args=(self.product.id, )))
        self.assertEqual(response.status_code, 200)

    def test_product_view_template(self):
        response = self.client.get(reverse('menu:show_product', args=(self.product.id, )))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('menu/product.html')

    def test_product_view_context(self):
        response = self.client.get(reverse('menu:show_product', args=(self.product.id, )))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('menu/product.html')
        self.assertEqual(self.product, response.context.get('product'))
        self.assertIn(self.category, response.context.get('categories'))
