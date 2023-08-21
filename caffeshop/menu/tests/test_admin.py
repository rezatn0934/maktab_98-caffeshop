from django.conf import settings
from django.contrib.admin.sites import AdminSite
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.db.models import Count

from menu.models import Product, Category
from orders.models import Order, Order_detail
from menu.admin import ProductAdmin, CategoryAdmin


class ModelAdminTests(TestCase):

    def setUp(self):
        self.product_image = open(settings.MEDIA_ROOT / "images/test/pina_colada.png", 'rb').read()
        self.category_image = open(settings.MEDIA_ROOT / "images/test/food.jpg", 'rb').read()
        self.category = Category.objects.create(name='Food',
                                                image=SimpleUploadedFile.from_dict(
                                                    {'filename': 'category_pic.png', 'content': self.category_image,
                                                     'content_tye': 'image/png'}))

        self.product = Product.objects.create(name='pepperoni',
                                              description="delicious pizza has many healthy ingredient and an special sauce to be disairable for you",
                                              category=self.category,
                                              price=10,
                                              image=SimpleUploadedFile.from_dict(
                                                  {'filename': 'product_pic.png', 'content': self.product_image,
                                                   'content_tye': 'image/png'}))

    def tearDown(self):
        self.product.delete()
        self.category.delete()

    def test_product_order_count_section_url(self):
        product_admin = ProductAdmin(Product, AdminSite())
        expected_link = f'<a href="/admin/orders/order_detail/?product__id={self.product.id}">{len(Order_detail.objects.filter(product=self.product))}</a>'
        query_set = Product.objects.filter(id=self.product.id).annotate(
            order_count=Count('order_detail__product')
        )
        product = query_set.get()
        given_link = product_admin.order_count(product)
        self.assertEqual(expected_link, given_link)

    def test_product_get_query_set(self):
        product_admin = ProductAdmin(Product, AdminSite())
        given_query_set = product_admin.get_queryset(self.client.request)
        self.assertTrue(hasattr(given_query_set.get(), 'order_count'))
        self.assertEqual(0, given_query_set.get().order_count)

    def test_product_admin_truncated_name(self):
        product_admin = ProductAdmin(Product, AdminSite())
        expected_text = "delicious pizza has many healthy ingredient and an special sauce …"
        given_text = product_admin.truncated_description(self.product)
        self.assertEqual(given_text, expected_text)

    def test_category_order_count_section_url(self):
        category_admin = CategoryAdmin(Category, AdminSite())
        expected_link = f'<a href="/admin/menu/product/?category__id={self.category.id}">{len(Product.objects.filter(category=self.category))}</a>'
        query_set = Category.objects.filter(id=self.category.id).annotate(
            product_count=Count('product')
        )
        category = query_set.get()
        given_link = category_admin.product_count(category)
        self.assertEqual(expected_link, given_link)

    def test_category_get_query_set(self):
        category_admin = CategoryAdmin(Category, AdminSite())
        given_query_set = category_admin.get_queryset(self.client.request)
        self.assertTrue(hasattr(given_query_set.get(), 'product_count'))
        self.assertEqual(1, given_query_set.get().product_count)
