
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from orders.models import Order, Order_detail, Table
from menu.models import Product, Category
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth.models import AnonymousUser
from model_bakery import baker
from orders.forms import OrderForm
from http.cookies import SimpleCookie
import json


class TestOrdersView(TestCase):
    def setUp(self):
        self.product = baker.make(Product)
        self.category = baker.make(Category)
        self.order = baker.make(Order)
        self.order_detail = Order_detail.objects.create(order=self.order, product=self.product, quantity=10)
        self.client = Client()
        self.table = Table.objects.create(name='nima', Table_number=55)
        return super().setUp()
    
    def tearDown(self):
        self.order_detail.delete()
        self.order.delete()
        self.category.delete()
        self.product.delete()
        self.table.delete()
        return super().tearDown()
    
    def test_cart_view_GET(self):
        response = self.client.get(reverse('orders:cart'))
        self.failUnless(response.context['form'],OrderForm)
        self.assertEqual(response.status_code, 200)

    def test_cart_view_POST_valid_data(self):
        response=self.client.post(reverse('orders:cart'), data={'phone_number':'09152593858',
                                                            'table':self.table.Table_number})
        self.assertRedirects(response, reverse('orders:create_order'), status_code=302, target_status_code=302, fetch_redirect_response=True)


    def test_cart_view_POST_invalid_data(self):
        response=self.client.post(reverse('orders:cart'), data={'phone_number':'0152593858',
                                                            'table':self.table.Table_number})
        self.assertRedirects(response, reverse('orders:cart'))


class TestOrderHistory(TestCase):
    def setUp(self) -> None:
        self.table = Table.objects.create(name='nima', Table_number=55)
        self.product = baker.make(Product)
        self.client = Client()
        self.client.cookies = SimpleCookie()
        self.client.cookies['orders'] = json.dumps({self.product.id:20})
        self.session = self.client.session
        self.session['pre_order'] = {'phone':'09152593858', 'table_number':self.table.Table_number}
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
        print(order_id_session)
        print()
        order_detail = Order_detail.objects.get(order=order_id_session)
        print(order_detail.product.name)
        print(self.product)
        print(order_detail.quantity)
        self.assertEqual(response.status_code, 200)

    def test_order_not_history(self):
        response = self.client.get(reverse('orders:order_history'))
        request = response.wsgi_request
        order_id_session = request.session.get('order_history')
        self.assertFalse(order_id_session)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['message'],"You Don't have any order yet.")