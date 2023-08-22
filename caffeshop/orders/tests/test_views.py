from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from orders.models import Order, Order_detail, Table
from django.test import TestCase, Client
from django.urls import reverse
from menu.models import Product, Category
from model_bakery import baker
from orders.forms import OrderForm
from http.cookies import SimpleCookie
import json


class TestOrdersView(TestCase):
    def setUp(self):
        self.image = open(settings.MEDIA_ROOT / "images/test/pina_colada.png", 'rb').read()
        self.product = baker.make(Product,
                                  image=SimpleUploadedFile.from_dict(
                                      {'filename': 'product_pic.png', 'content': self.image,
                                       'content_tye': 'image/png'}),
                                  name='Pina Colda')
        self.order = baker.make(Order)
        self.order_detail = Order_detail.objects.create(order=self.order, product=self.product, quantity=10)
        self.client = Client()
        self.client.cookies = SimpleCookie()
        self.client.cookies['orders'] = json.dumps(
            {self.product.id: {"price": float(self.product.price), "quantity": 10, "total_price": float(self.product.price) * 10}})
        self.table = Table.objects.create(name='nima', Table_number=55)
        return super().setUp()

    def tearDown(self):
        Order_detail.objects.all().delete()
        Product.objects.all().delete()
        Order.objects.all().delete()
        Table.objects.all().delete()
        return super().tearDown()

    def test_cart_view_GET(self):
        response = self.client.get(reverse('orders:cart'))
        self.failUnless(response.context['form'], OrderForm)
        self.assertEqual(response.status_code, 200)

    def test_cart_view_GET_with_phone(self):
        session = self.client.session
        session['user_phone'] = '09198470934'
        session.save()
        response = self.client.get(reverse('orders:cart'))
        self.failUnless(response.context['form'], OrderForm)
        self.assertEqual(response.status_code, 200)

    def test_cart_view_POST_valid_data(self):
        response = self.client.post(reverse('orders:cart'), data={'phone_number': '09152593858',
                                                                  'table_number': ''})
        self.assertRedirects(response, reverse('orders:create_order'), status_code=302, target_status_code=302,
                             fetch_redirect_response=True)

    def test_cart_view_POST_valid_data_and_table(self):
        response = self.client.post(reverse('orders:cart'), data={'phone_number': '09152593858',
                                                                  'table_number': self.table.id})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('orders:create_order'), fetch_redirect_response=False)

    def test_cart_view_POST_invalid_data(self):
        response = self.client.post(reverse('orders:cart'), data={'phone_number': '0152593858',
                                                                  'table': self.table.Table_number})
        self.assertRedirects(response, reverse('orders:cart'))


class TestOrderHistory(TestCase):
    def setUp(self):
        self.table = Table.objects.create(name='nima', Table_number=55)
        self.product = baker.make(Product)
        self.client = Client()
        self.client.cookies = SimpleCookie()
        self.client.cookies['orders'] = json.dumps(
            {self.product.id: {"price": float(self.product.price), "quantity": 10, "total_price": float(self.product.price) * 10}})
        self.session = self.client.session
        self.session['pre_order'] = {'phone': '09152593858', 'table_number': self.table.Table_number}
        self.session.save()
        return super().setUp()

    def tearDown(self) -> None:
        Order_detail.objects.all().delete()
        Product.objects.all().delete()
        Order.objects.all().delete()
        Table.objects.all().delete()
        del self.session
        return super().tearDown()

    def test_order_history(self):
        self.client.get(reverse('orders:create_order'))
        response = self.client.get(reverse('orders:order_history'))
        request = response.wsgi_request
        order_id_session = request.session.get('order_history')[0]
        order_detail = Order_detail.objects.get(order=order_id_session)
        self.assertEqual(response.status_code, 200)
        self.failUnless(order_detail)

    def test_order_has_tow_history(self):
        self.client.get(reverse('orders:create_order'))
        self.client.get(reverse('orders:order_history'))
        self.client.cookies['orders'] = json.dumps(
            {self.product.id: {"price": float(self.product.price), "quantity": 10,
                               "total_price": float(self.product.price) * 10}})

        self.session = self.client.session
        self.session['pre_order'] = {'phone': '09152593858', 'table_number': self.table.Table_number}
        self.session.save()
        self.client.get(reverse('orders:create_order'))
        response = self.client.get(reverse('orders:order_history'))

        request = response.wsgi_request
        order_id_session = request.session.get('order_history')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(order_id_session), 2)

    def test_order_not_history(self):
        response = self.client.get(reverse('orders:order_history'))
        request = response.wsgi_request
        order_id_session = request.session.get('order_history')
        self.assertFalse(order_id_session)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['message'], "You Don't have any order yet.")


class OrderCancellationTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.order = Order.objects.create(phone_number='1234567890', table_number=None)

    def test_cancel_order_by_customer(self):
        url = reverse('orders:cancel_order_by_customer', args=[self.order.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, 'C')
