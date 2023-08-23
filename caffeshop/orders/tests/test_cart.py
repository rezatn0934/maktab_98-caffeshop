from django.test import TestCase, Client
from orders.models import Table
from menu.models import Product, Category
from orders.cart import just_available_product
from model_bakery import baker
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
import os
from django.urls import reverse


class TestJustAvailableProduct(TestCase):
    def setUp(self):
        self.table = Table.objects.create(name='farzam', Table_number=1)
        self.table1 = Table.objects.create(name='reza', Table_number=2)
        self.image = open(settings.MEDIA_ROOT / "images/test/pina_colada.png", 'rb').read()
        self.product = baker.make(Product,
                                  image=SimpleUploadedFile.from_dict(
                                      {'filename': 'product_pic.png', 'content': self.image,
                                       'content_tye': 'image/png'}),
                                  name='Pina Colda', is_active=True)
        self.product1 = baker.make(Product,
                                   image=SimpleUploadedFile.from_dict(
                                       {'filename': 'product_pic1.png', 'content': self.image,
                                        'content_tye': 'image/png'}),
                                   name='test', is_active=False)
        self.parent_category = Category.objects.create(name='Food')
        self.category = Category.objects.create(name='fastfood', parent_category=self.parent_category)
        self.client = Client()

    def tearDown(self):
        Product.objects.all().delete()

        image_path = os.path.join(settings.MEDIA_ROOT / "images/product", "product_pic.png")
        if os.path.exists(image_path):
            os.remove(image_path)
        image_path1 = os.path.join(settings.MEDIA_ROOT / "images/product", "product_pic1.png")
        if os.path.exists(image_path1):
            os.remove(image_path1)

    def test_not_exist_products(self):
        order = {"100000000": {"price": float(self.product.price), "quantity": 10,
                               "total_price": float(self.product.price) * 10}}
        self.session = self.client.session
        self.session['pre_order'] = {'phone': '09152593858', 'table_number': self.table.Table_number}
        self.session.save()
        response = self.client.get(reverse("orders:create_order"))

        request = response.wsgi_request
        order_items, updated_orders = just_available_product(request, order)
        self.assertEqual(len(order_items), 0)
        self.assertEqual(updated_orders, {})

    def test_unavailable_products(self):
        order = {self.product1.id: {"price": float(self.product1.price), "quantity": 10,
                                    "total_price": float(self.product1.price) * 10}}
        self.session = self.client.session
        self.session['pre_order'] = {'phone': '09152593858', 'table_number': self.table1.Table_number}
        self.session.save()
        response = self.client.get(reverse("orders:create_order"))

        request = response.wsgi_request
        order_items, updated_orders = just_available_product(request, order)
        self.assertEqual(len(order_items), 0)
        self.assertEqual(updated_orders, {})
