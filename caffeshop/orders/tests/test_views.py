from django.test import SimpleTestCase, Client
from django.urls import reverse
from orders.models import *
import json

class TestUser(SimpleTestCase):
    
    def setUp(self):
        self.client = Client()
        self.cart_url = reverse('orders:cart')
        self.creat_order_url = reverse('orders:create_order')
        self.history_url = reverse('orders:order_history')
        self.cancle_order_url = reverse('orders:cancle_order_by_customer', args=['1'])


    def test_cart_view_GET(self):
        response= self.client.get(self.cart_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'templates/orders/cart.html')